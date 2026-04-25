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
    faculty: str
    purpose_location: str
    borrow_date: date
    return_date: date
    items: List[CartItem]

class EquipmentCreate(BaseModel):
    name: str
    description: str
    image_url: str
    total_quantity: int
    category: str

class NewsCreate(BaseModel):
    month_group: str
    day_string: str
    category: str
    title: str
    description: str
    href: str = "#"
    item_color: str = "#A259FF"
    icon_name: str = "NewspaperIcon"

class ActivityCreate(BaseModel):
    month_group: str
    time_seq: str
    phase: str
    title: str
    location_desc: str
    badge: Optional[str] = None
    item_color: str = "#A259FF"
    group_color: str = "#A259FF"
    icon_name: str = "CalendarDaysIcon"
    is_highlight: bool = False

class FacultyEquipmentCreate(BaseModel):
    name: str
    description: str
    image_url: str
    total_quantity: int
    faculty_id: str

class UpdateStatus(BaseModel):
    id: str
    status: str
