from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi_csrf_protect import CsrfProtect
from pydantic import BaseModel
from db.database import supabase

router = APIRouter()

# 📦 โครงสร้างข้อมูลอุปกรณ์ (Schema)
class EquipmentCreate(BaseModel):
    name: str
    description: str
    image_url: str
    total_quantity: int
    category: str

# 📰 โครงสร้างข้อมูลข่าวสาร (Schema)
class NewsCreate(BaseModel):
    month_group: str
    day_string: str
    category: str
    title: str
    description: str
    href: str = "#"
    item_color: str = "#A259FF"
    icon_name: str = "NewspaperIcon"

# (💡 แนะนำ: ในระบบจริง ควรเขียนเช็คด้วยว่าคนที่ยิง API นี้มีสถานะเป็น Admin จริงๆ หรือไม่)

@router.post('/admin/equipment')
async def create_equipment(request: Request, req: EquipmentCreate, csrf_protect: CsrfProtect = Depends()):
    await csrf_protect.validate_csrf(request)
    try:
        # เตรียมข้อมูล โดยเซ็ต available ให้เท่ากับ total ตอนสร้างใหม่
        data = req.dict()
        data["available_quantity"] = req.total_quantity 
        
        supabase.table("equipments").insert(data).execute()
        return {"status": "success", "message": "เพิ่มครุภัณฑ์ใหม่เรียบร้อย"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/admin/news')
async def create_news(request: Request, req: NewsCreate, csrf_protect: CsrfProtect = Depends()):
    await csrf_protect.validate_csrf(request)
    try:
        supabase.table("news").insert(req.dict()).execute()
        return {"status": "success", "message": "ประกาศข่าวสารเรียบร้อย"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))