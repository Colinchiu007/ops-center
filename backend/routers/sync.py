"""Config file generation and sync endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from middleware.auth import require_admin
from services import config_service, file_writer

router = APIRouter(prefix="/api/v1/sync", tags=["sync"])


@router.post("/feature-gates")
async def sync_feature_gates(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(require_admin),
):
    """Generate feature_gates.yaml from DB and write to disk."""
    items = await config_service.get_configs_by_category(db, "feature_flag")
    if not items:
        raise HTTPException(400, "No feature gates found in database")

    path = file_writer.write_feature_gates(items)
    return {
        "status": "ok",
        "path": path,
        "gates": len(items),
        "message": f"Written {len(items)} feature gates to {path}"
    }


@router.get("/status")
async def sync_status(db: AsyncSession = Depends(get_db)):
    """Check sync status across all projects."""
    projects = await config_service.get_all_projects(db)
    import os
    result = []
    for p in projects:
        items = await config_service.get_configs_by_project(db, p.code)
        file_exists = os.path.exists(p.config_file_path) if p.config_file_path else False
        result.append({
            "project": p.code,
            "config_file": p.config_file_path,
            "file_exists": file_exists,
            "items_in_db": len(items),
        })
    return {"projects": result}
