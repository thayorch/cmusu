from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
import os
from dotenv import load_dotenv

# Import สิ่งที่เราแยกไฟล์ไว้
from core.config import CsrfSettings
from routers import reports

load_dotenv()

# โหลดการตั้งค่า CSRF
@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

app = FastAPI(
    title="CMUSU Backend",
    description="Developed by thayorch",
    version="1.0.0"
)

# --- CORS configuration ---
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,        
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
    allow_headers=["Authorization", "Content-Type", "X-CSRF-Token"],
)

# --- Exception Handler สำหรับ CSRF ---
@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

# ==========================================
# นำ Router ที่แยกไว้มาเชื่อมต่อกับ App หลัก
# ==========================================
app.include_router(reports.router, prefix="/api", tags=["Reports"])


@app.get("/api/health")
async def health_check():
    return {"status": "OK", "message": "Server is running smoothly"}

@app.get("/")
async def root():
    return {"message": "Welcome to CMUSU backend!!", "health": "/api/health"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)