from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect

router = APIRouter()

@router.get("/csrf-token")
async def get_csrf(csrf_protect: CsrfProtect = Depends()):
    """ Endpoint สำหรับให้ Frontend ขอ CSRF Token """
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens() 
    response = JSONResponse({"csrf_token": csrf_token})
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response