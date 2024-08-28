from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from src.core.data.registry import domain_registry
from api.config import config

router = APIRouter()


@router.get("/catalog/{object_type}/{object_id}")
async def get_object(object_type: str, object_id: str):
    if not DomainObjectRegistry.is_registered(object_type):
        raise HTTPException(status_code=404, detail=f"Unknown object type: {object_type}")

    accessor = domain_registry.get_accessor(object_type)
    obj = await accessor.get_by_id(object_id)

    if obj:
        return obj
    raise HTTPException(status_code=404, detail=f"{object_type} not found")


@router.post("/catalog/{object_type}")
async def create_object(object_type: str, obj_data: Dict[str, Any]):
    if not domain_registry.is_registered(object_type):
        raise HTTPException(status_code=404, detail=f"Unknown object type: {object_type}")

    domain_class = domain_registry.get_domain_object(object_type)
    accessor = domain_registry.get_accessor(object_type)
    obj = domain_class(**obj_data)
    created_obj = await accessor.create(obj)
    return created_obj


@router.put("/catalog/{object_type}/{object_id}")
async def update_object(object_type: str, object_id: str, obj_data: Dict[str, Any]):
    if not domain_registry.is_registered(object_type):
        raise HTTPException(status_code=404, detail=f"Unknown object type: {object_type}")

    domain_class = domain_registry.get_domain_object(object_type)
    accessor = domain_registry.get_accessor(object_type)
    existing_obj = await accessor.get_by_id(object_id)

    if not existing_obj:
        raise HTTPException(status_code=404, detail=f"{object_type} not found")

    updated_obj = domain_class(**{**existing_obj.dict(), **obj_data, "id": object_id})
    result = await accessor.update(updated_obj)
    return result


@router.delete("/catalog/{object_type}/{object_id}")
async def delete_object(object_type: str, object_id: str):
    if not domain_registry.is_registered(object_type):
        raise HTTPException(status_code=404, detail=f"Unknown object type: {object_type}")

    accessor = domain_registry.get_accessor(object_type)
    deleted = await accessor.delete(object_id)

    if deleted:
        return {"message": f"{object_type} deleted successfully"}
    raise HTTPException(status_code=404, detail=f"{object_type} not found")


@router.get("/catalog/types")
async def get_registered_types():
    return {"registered_types": domain_registry.get_all_types()}