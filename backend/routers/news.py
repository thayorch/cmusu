from fastapi import APIRouter
from db.database import supabase

router = APIRouter()

@router.get('/news')
async def get_news():
    """ Endpoint ดึงข้อมูลข่าวสารจาก Supabase """
    try:
        response = supabase.table("news").select("*").order("created_at", desc=True).execute()
        raw_data = response.data
        
        grouped_data = {}
        for row in raw_data:
            month = row["month_group"]
            if month not in grouped_data:
                grouped_data[month] = {
                    "month": month,
                    "color": row["item_color"],
                    "events": []
                }
            
            grouped_data[month]["events"].append({
                "id": str(row["id"]),
                "day": row["day_string"],
                "category": row["category"],
                "icon": row["icon_name"],
                "title": row["title"],
                "desc": row["description"],
                "color": row["item_color"],
                "highlight": row["is_highlight"],
                "href": row["href"] if row["href"] else "#"
            })
            
        final_data = list(grouped_data.values())
        return {
            "status": "success",
            "message": "ดึงข้อมูลข่าวสารสำเร็จ",
            "data": final_data
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "data": []}