from fastapi import HTTPException, Request, Depends
from db.database import supabase

async def get_current_user_role(request: Request):
    """ ตรวจสอบ User และดึง Role จาก app_metadata """
    token = request.cookies.get("access_token") 
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        user_res = supabase.auth.get_user(token)
        if not user_res.user:
            raise HTTPException(status_code=401, detail="Invalid session")
        role = user_res.user.app_metadata.get("role", "user")
        return role
    except Exception:
        raise HTTPException(status_code=401, detail="Authentication failed")

async def admin_required(role: str = Depends(get_current_user_role)):
    """ ด่านกั้น: ถ้าไม่ใช่ admin จะส่ง 403 ทันที """
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return role