from fastapi import APIRouter, BackgroundTasks, Depends, Request, HTTPException
from fastapi_csrf_protect import CsrfProtect
from db.database import supabase
from models.schemas import BorrowSubmit
from utils.email import send_status_email

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
async def submit_borrow_request(
    request: Request,
    req: BorrowSubmit,
    background_tasks: BackgroundTasks,
    csrf_protect: CsrfProtect = Depends(),
):
    await csrf_protect.validate_csrf(request)

    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        user_res = supabase.auth.get_user(token)
        user = user_res.user
        user_id = user.id
        user_email = user.email or ""
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

        supabase.rpc("checkout_borrow_cart", rpc_payload).execute()

        eq_ids = [item.equipment_id for item in req.items]
        eq_res = supabase.table("equipments").select("id, name, image_url").in_("id", eq_ids).execute()
        eq_map = {row["id"]: row for row in eq_res.data}

        email_items = [
            {
                "name": eq_map.get(item.equipment_id, {}).get("name", ""),
                "image_url": eq_map.get(item.equipment_id, {}).get("image_url", ""),
                "quantity": item.quantity,
            }
            for item in req.items
        ]

        if user_email:
            background_tasks.add_task(
                send_status_email,
                to_email=user_email,
                full_name=req.full_name,
                status="pending",
                borrow_date=str(req.borrow_date),
                return_date=str(req.return_date),
                items=email_items,
            )

        return {"status": "success", "message": "ส่งคำร้องขอยืมสำเร็จ รอการอนุมัติ"}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/borrow/faculty/{faculty_id}')
async def get_faculty_data(faculty_id: str):
    try:
        res = supabase.table("faculties_equipments").select("*").eq("faculty_id", faculty_id).execute()
        return {"status": "success", "data": res.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

    