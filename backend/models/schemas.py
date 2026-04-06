from pydantic import BaseModel
from typing import Optional

class ReportSubmit(BaseModel):
    userType: str
    topicType: str
    title: str
    description: str
    contactInfo: Optional[str] = ""