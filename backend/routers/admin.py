from fastapi import APIRouter, BackgroundTasks, Depends, Request, HTTPException, UploadFile, File
from fastapi_csrf_protect import CsrfProtect
from pydantic import BaseModel
import uuid
import traceback
from db.database import supabase
from dependencies import admin_required

from models.schemas import EquipmentCreate, NewsCreate, UpdateStatus
from utils.email import send_status_email


# 💡 ทริค: ใส่ด่านตรวจ admin_required ไว้ที่ Router หลักเลย 
# ทุก API ในไฟล์นี้จะต้องผ่านการเช็คว่าเป็น Admin เท่านั้นถึงจะเข้าได้!
router = APIRouter(dependencies=[Depends(admin_required)])

# ==========================================
# 🗂️ 1. หมวดจัดการครุภัณฑ์ (Equipments)
# ==========================================

@router.get('/admin/equipment')
async def get_all_equipment():
    """ ดึงรายการครุภัณฑ์ทั้งหมด (แสดงในตาราง) """
    try:
        res = supabase.table("equipments").select("*").order("created_at", desc=True).execute()
        return {"status": "success", "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/admin/equipment')
async def create_equipment(request: Request, req: EquipmentCreate, csrf_protect: CsrfProtect = Depends()):
    """ เพิ่มรายการครุภัณฑ์ใหม่ """
    await csrf_protect.validate_csrf(request)
    try:
        data = req.dict()
        data["available_quantity"] = req.total_quantity 
        supabase.table("equipments").insert(data).execute()
        return {"status": "success", "message": "เพิ่มครุภัณฑ์ใหม่เรียบร้อย"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/admin/equipment/{equipment_id}')
async def update_equipment(request: Request, equipment_id: str, req: EquipmentCreate, csrf_protect: CsrfProtect = Depends()):
    """ แก้ไขข้อมูลครุภัณฑ์ และคำนวณสต๊อกใหม่ """
    await csrf_protect.validate_csrf(request)
    try:
        current_eq = supabase.table("equipments").select("total_quantity", "available_quantity").eq("id", equipment_id).single().execute()
        
        old_total = current_eq.data["total_quantity"]
        old_available = current_eq.data["available_quantity"]

        diff = req.total_quantity - old_total
        new_available = old_available + diff

        if new_available < 0:
            raise HTTPException(status_code=400, detail="ไม่สามารถลดจำนวนรวมต่ำกว่าจำนวนที่มีคนยืมอยู่ได้")

        update_data = req.dict()
        update_data["available_quantity"] = new_available

        supabase.table("equipments").update(update_data).eq("id", equipment_id).execute()
        return {"status": "success", "message": "อัปเดตข้อมูลเรียบร้อย"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/admin/equipment/{equipment_id}')
async def delete_equipment(request: Request, equipment_id: str, csrf_protect: CsrfProtect = Depends()):
    """ ลบรายการครุภัณฑ์ """
    await csrf_protect.validate_csrf(request)
    try:
        supabase.table("equipments").delete().eq("id", equipment_id).execute()
        return {"status": "success", "message": "ลบครุภัณฑ์เรียบร้อย"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# 📋 2. หมวดจัดการรายการยืม-คืน (Borrow Requests)
# ==========================================
# 💡 แก้ไขแค่ฟังก์ชันนี้ฟังก์ชันเดียวครับ
@router.get('/admin/requests')
async def get_all_requests():
    """ ดึงรายการคำร้องทั้งหมด พร้อมรายการอุปกรณ์และรูปภาพที่ยืม """
    try:
        # เพิ่ม image_url เข้าไปตรง equipments(...) 
        res = supabase.table("borrow_requests") \
            .select("*, borrow_request_items(quantity, equipments(name, image_url))") \
            .order("created_at", desc=True) \
            .execute()
        return {"status": "success", "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put('/admin/requests/status')
async def update_request_status(
    request: Request,
    payload: UpdateStatus,
    background_tasks: BackgroundTasks,
    csrf_protect: CsrfProtect = Depends(),
):
    """ อัปเดตสถานะคำร้อง และส่งอีเมลแจ้งผู้ยืม """
    await csrf_protect.validate_csrf(request)
    try:
        req_data = supabase.table("borrow_requests") \
            .select("user_id, full_name, borrow_date, return_date") \
            .eq("id", payload.id).single().execute()

        supabase.table("borrow_requests").update({"status": payload.status}).eq("id", payload.id).execute()

        # ดึงรายการอุปกรณ์พร้อมชื่อและรูปสำหรับอีเมล
        items_with_names = supabase.table("borrow_request_items") \
            .select("quantity, equipments(name, image_url)") \
            .eq("request_id", payload.id).execute()
        email_items = [
            {
                "name": item["equipments"]["name"],
                "image_url": item["equipments"].get("image_url", ""),
                "quantity": item["quantity"],
            }
            for item in items_with_names.data
            if item.get("equipments")
        ]

        if payload.status == "returned":
            stock_items = supabase.table("borrow_request_items") \
                .select("equipment_id, quantity").eq("request_id", payload.id).execute()
            for item in stock_items.data:
                eq_id = item["equipment_id"]
                qty = item["quantity"]
                current_eq = supabase.table("equipments").select("available_quantity").eq("id", eq_id).single().execute()
                new_qty = current_eq.data["available_quantity"] + qty
                supabase.table("equipments").update({"available_quantity": new_qty}).eq("id", eq_id).execute()

        # ส่งอีเมลแจ้งผู้ยืมใน Background (ไม่ block response)
        try:
            user_id = req_data.data["user_id"]
            user_res = supabase.auth.admin.get_user_by_id(user_id)
            to_email = user_res.user.email
            if to_email:
                background_tasks.add_task(
                    send_status_email,
                    to_email=to_email,
                    full_name=req_data.data["full_name"],
                    status=payload.status,
                    borrow_date=str(req_data.data["borrow_date"]),
                    return_date=str(req_data.data["return_date"]),
                    items=email_items,
                )
        except Exception as email_err:
            print(f"⚠️ Could not resolve email for notification: {email_err}")

        return {"status": "success", "message": f"เปลี่ยนสถานะเป็น {payload.status} เรียบร้อย"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/admin/requests/{request_id}')
async def delete_request(request: Request, request_id: str, csrf_protect: CsrfProtect = Depends()):
    """ ลบคำร้องขอยืม """
    await csrf_protect.validate_csrf(request)
    try:
        # ลบข้อมูล (ด้วย ON DELETE CASCADE ใน SQL ข้อมูลในตารางไอเทมที่ยืมจะถูกลบไปด้วย)
        supabase.table("borrow_requests").delete().eq("id", request_id).execute()
        return {"status": "success", "message": "ลบคำร้องเรียบร้อยแล้ว"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# 🖼️ 3. หมวดจัดการอัปโหลดไฟล์ (Uploads)
# ==========================================

@router.post('/admin/upload')
async def upload_image(request: Request, file: UploadFile = File(...), csrf_protect: CsrfProtect = Depends()):
    """ อัปโหลดรูปภาพเข้า Supabase Storage และคืนค่า URL """
    await csrf_protect.validate_csrf(request)
    try:
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_bytes = await file.read()

        res = supabase.storage.from_("equipment-images").upload(
            path=unique_filename, 
            file=file_bytes, 
            file_options={"content-type": file.content_type}
        )
        
        public_url = supabase.storage.from_("equipment-images").get_public_url(unique_filename)
        return {"status": "success", "url": public_url}
    
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดตอนอัปโหลด: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# 📰 4. หมวดจัดการข่าวสาร (News)
# ==========================================

@router.post('/admin/news')
async def create_news(request: Request, req: NewsCreate, csrf_protect: CsrfProtect = Depends()):
    """ เพิ่มข่าวสารใหม่ """
    await csrf_protect.validate_csrf(request)
    try:
        supabase.table("news").insert(req.dict()).execute()
        return {"status": "success", "message": "ประกาศข่าวสารเรียบร้อย"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# 📢 5. หมวดจัดการเสียงสะท้อน (VOC)
# ==========================================

@router.get('/admin/reports')
async def get_all_reports():
    """ ดึงรายการข้อร้องเรียน (VOC) ทั้งหมด แสดงในหน้า Admin """
    try:
        res = supabase.table("reports").select("*").order("created_at", desc=True).execute()
        return {"status": "success", "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

