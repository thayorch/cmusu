from fastapi import APIRouter, Response, Request
from fastapi.responses import RedirectResponse
from db.database import supabase
from typing import Optional
import os

router = APIRouter()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

@router.get("/auth/login")
async def login():
    """ สร้าง URL ไปยังหน้า Login ของ Microsoft ผ่าน Supabase """
    res = supabase.auth.sign_in_with_oauth({
        "provider": "azure",
        "options": {
            "redirect_to": f"{BACKEND_URL}/api/auth/callback" ,
            "scopes": "email profile"  
        }
    })
    return RedirectResponse(url=res.url)

@router.get("/auth/callback")
async def callback(code: Optional[str] = None):
    """ รับ Code มาแลกเป็น Access Token แล้วฝังลง HTTP-Only Cookie """
    # ถ้าไม่มี code (เช่น ผู้ใช้เข้าลิงก์มั่ว) ให้เตะกลับไปหน้าแรก
    if not code:
        return RedirectResponse(url=f"{FRONTEND_URL}/?error=missing_code")

    try:
        session = supabase.auth.exchange_code_for_session({"auth_code": code})
        access_token = session.session.access_token
        
        response = RedirectResponse(url=f"{FRONTEND_URL}/borrow-central")
        # ฝัง Token ป้องกัน XSS
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=3600
        )
        return response
    except Exception as e:
        print("Auth Error:", e)
        return RedirectResponse(url=f"{FRONTEND_URL}/?error=login_failed")

@router.get("/auth/me")
async def get_current_user(request: Request):
    """ อ่าน Cookie เพื่อดึงข้อมูล User ปัจจุบัน """
    token = request.cookies.get("access_token")
    if not token:
        return {"user": None}
    try:
        user_res = supabase.auth.get_user(token)
        return {"user": user_res.user}
    except Exception:
        return {"user": None}


@router.post("/auth/logout")
async def logout(response: Response):
    """ ลบ Cookie เพื่อออกจากระบบ """
    response.delete_cookie("access_token")
    return {"status": "success", "message": "Logged out"}