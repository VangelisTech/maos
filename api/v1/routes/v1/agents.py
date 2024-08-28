from fastapi import APIRouter, Depends

from maf.api.dependencies import get_current_user
from fastapi import APIRouter, Depends

from maf.api.dependencies import get_current_user

router = APIRouter()


async def get_agent(current_user: dict = Depends(get_current_user)): )
    # Implement agent listing logic
    return []

@router.get("agent/{agent.id}/completion", response_model=)
async def acompletion

@router.post("/agents/create", response_model=Agent)
async def create_agent(agent: Agent, current_user: dict = Depends(get_current_user)):
    # Implement agent creation logic
    return agent