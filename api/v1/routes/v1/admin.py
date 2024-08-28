from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from maf.api.dependencies import get_current_admin_user
from maf.core.models import User, Invite, Workspace, WorkspaceChat, SystemSettings
from maf.core.security import get_password_hash

router = APIRouter(prefix="/v1/admin", tags=["Admin"])



@router.get("/is-multi-user-mode")
async def is_multi_user_mode():
    # Implement logic to check if multi-user mode is enabled
    return {"isMultiUser": True}

@router.get("/users")
async def get_users(current_user: User = Depends(get_current_admin_user)):
    users = await User.get_all()
    return {"users": users}

@router.post("/users/new")
async def create_user(user: UserCreate, current_user: User = Depends(get_current_admin_user)):
    hashed_password = get_password_hash(user.password)
    new_user = await User.create(username=user.username, hashed_password=hashed_password, role=user.role)
    return {"user": new_user, "error": None}

@router.post("/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, current_user: User = Depends(get_current_admin_user)):
    # Implement logic to update user
    updated_user = await User.update(user_id, user_update.dict(exclude_unset=True))
    return {"success": True, "error": None}

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, current_user: User = Depends(get_current_admin_user)):
    await User.delete(user_id)
    # Implement logic to log event
    return {"success": True, "error": None}

@router.get("/invites")
async def get_invites(current_user: User = Depends(get_current_admin_user)):
    invites = await Invite.get_all_with_users()
    return {"invites": invites}

@router.post("/invite/new")
async def create_invite(invite: InviteCreate, current_user: User = Depends(get_current_admin_user)):
    new_invite = await Invite.create(workspaceIds=invite.workspaceIds)
    return {"invite": new_invite, "error": None}

@router.delete("/invite/{invite_id}")
async def deactivate_invite(invite_id: int, current_user: User = Depends(get_current_admin_user)):
    success = await Invite.deactivate(invite_id)
    return {"success": success, "error": None}

@router.get("/workspaces/{workspace_id}/users")
async def get_workspace_users(workspace_id: int, current_user: User = Depends(get_current_admin_user)):
    users = await Workspace.get_users(workspace_id)
    return {"users": users}

@router.post("/workspaces/{workspace_id}/update-users")
async def update_workspace_users(workspace_id: int, user_update: WorkspaceUserUpdate, current_user: User = Depends(get_current_admin_user)):
    success = await Workspace.update_users(workspace_id, user_update.userIds)
    return {"success": success, "error": None}

@router.post("/workspace-chats")
async def get_workspace_chats(offset: int = 0, current_user: User = Depends(get_current_admin_user)):
    chats, has_more = await WorkspaceChat.get_paginated(offset=offset, limit=20)
    return {"chats": chats, "hasPages": has_more}

@router.get("/preferences")
async def get_preferences(current_user: User = Depends(get_current_admin_user)):
    settings = await SystemSettings.get_all()
    return {"settings": settings}

@router.post("/preferences")
async def update_preferences(preferences: SystemPreferences, current_user: User = Depends(get_current_admin_user)):
    await SystemSettings.update(preferences.dict())
    return {"success": True, "error": None}