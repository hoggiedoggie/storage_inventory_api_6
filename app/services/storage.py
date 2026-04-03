from uuid import UUID
from datetime import datetime
from typing import List, Tuple, Optional
from app.models.storage import StorageDevice
from app.schemas.storage import StorageCreate, StorageUpdate
from app.services.cache import cache_service

class StorageService:
    model = StorageDevice

    def _get_device_dict(self, device: StorageDevice) -> dict:
        return {
            "id": str(device.id),
            "model": device.model,
            "serial_number": device.serial_number,
            "capacity_gb": device.capacity_gb,
            "status": device.status,             
            "user_id": str(device.user_id),
            "created_at": device.created_at.isoformat() if device.created_at else None,
            "updated_at": device.updated_at.isoformat() if device.updated_at else None,
        }

    async def get(self, id: UUID) -> Optional[StorageDevice]:

        cache_key = f"items:id:{id}"
        
        cached_device = cache_service.get(cache_key)
        if cached_device:
            return cached_device

        device = await self.model.find_one(
            self.model.id == id, 
            self.model.deleted_at == None
        )

        if device:
            cache_service.set(cache_key, self._get_device_dict(device))
            
        return device

    async def get_multi_by_owner(self, *, user_id: UUID, page: int, limit: int) -> Tuple[List[dict], int]:

        cache_key = f"items:list:user:{user_id}:page:{page}:limit:{limit}"

        cached_result = cache_service.get(cache_key)
        if cached_result:
            return cached_result["items"], cached_result["total"]

        query = self.model.find(
            self.model.user_id == user_id, 
            self.model.deleted_at == None
        )
        
        total = await query.count()

        items = await query.skip((page - 1) * limit).limit(limit).to_list()
        
        items_dict = [self._get_device_dict(item) for item in items]
        
        cache_service.set(cache_key, {"items": items_dict, "total": total})
        
        return items_dict, total

    async def create_with_owner(self, *, obj_in: StorageCreate, user_id: UUID) -> StorageDevice:
 
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, user_id=user_id)
        
        await db_obj.insert()
        
        cache_service.delete_by_pattern(f"items:list:user:{user_id}:*")
        
        return db_obj

    async def update(self, *, db_obj: StorageDevice, obj_in: StorageUpdate) -> StorageDevice:

        update_data = obj_in.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        await db_obj.set(update_data)
        
        cache_service.delete(f"items:id:{db_obj.id}")
        cache_service.delete_by_pattern(f"items:list:user:{db_obj.user_id}:*")
        
        return db_obj

    async def remove(self, id: UUID) -> Optional[StorageDevice]:
 
        obj = await self.model.find_one(
            self.model.id == id, 
            self.model.deleted_at == None
        )
        
        if obj:
            user_id = obj.user_id
            obj.deleted_at = datetime.utcnow()
            await obj.save()
 
            cache_service.delete(f"items:id:{id}")
            cache_service.delete_by_pattern(f"items:list:user:{user_id}:*")
            
        return obj

storage_service = StorageService()