from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from models.schemas import ReportSubmit
from db.database import supabase
router = APIRouter()

@router.post("/report")
async def submit_report(
    request: Request, 
    report: ReportSubmit, 
    csrf_protect: CsrfProtect = Depends()
):
    """ Endpoint สำหรับรับข้อมูลแบบฟอร์ม VOC พร้อมบันทึกลง Supabase """
    # ตรวจสอบ CSRF Token
    await csrf_protect.validate_csrf(request)
    
    # จัดเตรียมข้อมูลตาม Column ในฐานข้อมูล
    report_data = {
        "user_type": report.userType,
        "topic_type": report.topicType,
        "title": report.title,
        "description": report.description,
        "contact_info": report.contactInfo,
    }

    try:
        # เช็คว่าเชื่อมต่อ Database ได้หรือไม่
        if not supabase:
            return JSONResponse(status_code=500, content={"detail": "Database connection is not configured."})
            
        # บันทึกข้อมูลลงตาราง reports ใน Supabase
        result = supabase.table("reports").insert(report_data).execute()
        
        return {
            "status": "success",
            "message": "บันทึกข้อมูลการร้องเรียนสำเร็จ",
            "data": result.data
        }

    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"detail": f"ไม่สามารถบันทึกข้อมูลได้: {str(e)}"})
        