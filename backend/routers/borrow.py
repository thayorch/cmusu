from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi_csrf_protect import CsrfProtect
from db.database import supabase
from models.schemas import BorrowSubmit

router = APIRouter()

@router.get('/equipments/central')
async def get_central_equipments():
    """ ดึงรายการครุภัณฑ์ส่วนกลางทั้งหมด """
    try:
        res = supabase.table("equipments").select("*").eq("category", "ส่วนกลาง").execute()
        return {"status": "success", "data": res.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
        
@router.post('/borrow/request')
async def submit_borrow_request(request: Request, req: BorrowSubmit, csrf_protect: CsrfProtect = Depends()):
    await csrf_protect.validate_csrf(request)
    
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    try:
        user_res = supabase.auth.get_user(token)
        user_id = user_res.user.id
    except:
        raise HTTPException(status_code=401, detail="Invalid Session")

    try:
        rpc_payload = {
            "p_user_id": user_id,
            "p_full_name": req.full_name,
            "p_student_id": req.student_id,
            "p_contact_info": req.contact_info,
            "p_faculty": req.faculty,
            "p_purpose_location": req.purpose_location,
            "p_borrow_date": str(req.borrow_date),
            "p_return_date": str(req.return_date),
            "p_items": [item.dict() for item in req.items]
        }
        
        res = supabase.rpc("checkout_borrow_cart", rpc_payload).execute()
        
        return {"status": "success", "message": "ส่งคำร้องขอยืมสำเร็จ รอการอนุมัติ"}
        
    except Exception as e:
        # ถ้าของหมด หรือมี Error ระบบจะเด้งมาตรงนี้
        raise HTTPException(status_code=400, detail=str(e))