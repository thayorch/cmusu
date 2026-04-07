from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class ReportSubmit(BaseModel):
    userType: str
    topicType: str
    title: str
    description: str
    contactInfo: Optional[str] = ""

class CartItem(BaseModel):
    equipment_id: str
    quantity: int

class BorrowSubmit(BaseModel):
    full_name: str
    student_id: str
    contact_info: str
    borrow_date: date
    return_date: date
    items: List[CartItem] 