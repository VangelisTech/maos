from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, List
from pydantic import BaseModel
import uuid
from maf.core.session_manager import SessionManager  # Assume this exists in your core module

router = APIRouter()
security = HTTPBearer()
session_manager = SessionManager()



def token_required(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Implement your token verification logic here
    # For example:
    if not is_token_valid(credentials.credentials):
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials.credentials

def is_token_valid(token: str) -> bool:
    # Implement your token validation logic here
    # This is just a placeholder
    return True

@router.get("/api/sessions", response_model=List[Session])
async def get_sessions(current_user: str = Depends(token_required)):
    return session_manager.list_sessions()

@router.post("/api/sessions", response_model=SessionResponse, status_code=201)
async def create_session(session: SessionCreate, current_user: str = Depends(token_required)):
    session_id = session_manager.create_session()
    return SessionResponse(sessionId=session_id)

@router.get("/api/sessions/{session_id}", response_model=Session)
async def get_session(session_id: str, current_user: str = Depends(token_required)):
    session = session_manager.get_session(session_id)
    if session:
        return session
    raise HTTPException(status_code=404, detail="Session not found")

@router.delete("/api/sessions/{session_id}", response_model=Dict[str, str])
async def delete_session(session_id: str, current_user: str = Depends(token_required)):
    result = session_manager.delete_session(session_id)
    if result:
        return {"message": "Session deleted"}
    raise HTTPException(status_code=404, detail="Session not found")