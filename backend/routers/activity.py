from fastapi import APIRouter
from db.database import supabase

router = APIRouter()

@router.get('/activity')
async def get_activity():
    """ Endpoint ดึงข้อมูลตารางกิจกรรม """
    try:
        response = supabase.table("activities").select("*").order("time_seq").execute()
        raw_data = response.data
        
        grouped_data = {}
        for row in raw_data:
            month = row["month_group"]
            if month not in grouped_data:
                grouped_data[month] = {
                    "month": month,
                    "color": row["group_color"],
                    "events": []
                }
            
            grouped_data[month]["events"].append({
                "time": row["time_seq"],
                "phase": row["phase"],
                "icon": row["icon_name"],
                "title": row["title"],
                "desc": row["location_desc"],
                "color": row["item_color"],
                "highlight": row["is_highlight"],
                "badge": row["badge"] if row["badge"] else None
            })
            
        final_data = list(grouped_data.values())

        return {
            "status": "success",
            "message": "ดึงข้อมูลตารางกิจกรรมสำเร็จ",
            "data": final_data
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "data": []}