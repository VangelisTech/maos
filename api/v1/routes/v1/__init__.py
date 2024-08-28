from fastapi import APIRouter
from . import artifacts, tasks, domain_object_catalog, agents

router = APIRouter()

router.include_router(artifacts.router, prefix="/artifacts", tags=["artifacts"])
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
router.include_router(unity_catalog.router, prefix="/unity-catalog", tags=["unity-catalog"])
router.include_router(agents.router, prefix="/agents", tags=["agents"])