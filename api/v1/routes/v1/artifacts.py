from typing import Optional, Dict, Any

from fastapi import APIRouter, UploadFile
from maf.schema.base import UserSession, Artifact

router = APIRouter(prefix="/artifacts", tags=["artifacts"])

@router.post("/artifact/upload")
async def upload_artifact(
    file: UploadFile,
    metadata: Optional[Dict[str,Any]],
    version: Optional[str]
    session: UserSession,

):
    file_content = await file.read()
    
    get_bucket( ) 
    artifact = Artifact(
        name = file.filename,
        metadata = metadata,
        

        account_id = session.account_id,
        user_id = session.user_id,
        payload = file_content
        size_bytes=len(file_content)

    )

    stored_artifact = artifact_storage.save_artifact(artifact, file_content)



    return {"status": "processing", "artifact_id": stored_artifact.id}

@router.get("/artifacts", response_model=List[Artifact])
async def get_artifact(current_user: dict = Depends(get_current_user)):
    return []

@router.get("/artifact/{artifact_id}", response_model=List[Artifact])
async def get_artifact(current_user: dict = Depends(get_current_user)):
    # Implement artifact listing logic
    return []