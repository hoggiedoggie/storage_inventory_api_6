from fastapi import APIRouter, Depends, HTTPException, Query, status
from uuid import UUID
from typing import List, Optional

from app.api.v1.deps import get_current_user
from app.models.user import User
from app.services.storage import storage_service
from app.schemas.storage import StorageCreate, StorageUpdate, StorageResponse, StorageListResponse

router = APIRouter(tags=["Storage"])

@router.get("/", response_model=StorageListResponse)
async def read_devices(
 
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    items, total = await storage_service.get_multi_by_owner(
        user_id=current_user.id, page=page, limit=limit
    )
    
    total_pages = (total + limit - 1) // limit
    return {
        "data": items,
        "meta": {
            "total": total, 
            "page": page, 
            "limit": limit, 
            "totalPages": total_pages
        }
    }

@router.post("/", response_model=StorageResponse, status_code=status.HTTP_201_CREATED)
async def create_device(
    obj_in: StorageCreate, 
    current_user: User = Depends(get_current_user)
):
    return await storage_service.create_with_owner(
        obj_in=obj_in, 
        user_id=current_user.id
    )

@router.get("/{id}", response_model=StorageResponse)
async def read_device(
    id: UUID, 
    current_user: User = Depends(get_current_user)
):
    
    device = await storage_service.get(id=id)
    
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    owner_id = device.user_id if not isinstance(device, dict) else device["user_id"]
    
    if str(owner_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Forbidden")
        
    return device