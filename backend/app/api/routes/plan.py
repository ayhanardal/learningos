from fastapi import APIRouter, Response
from app.services import data

router = APIRouter(prefix="/plan")

@router.get("/roadmap")
async def get_plan_roadmap(response: Response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    try:
        return data.get_plan_roadmap()
    except Exception as e:
        print(f"[api] Error in get_plan_roadmap: {e}")
        return {"error": str(e), "data": []}

@router.get("/adequacy")
async def get_adequacy(response: Response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    try:
        from app.services.plan_generator import get_adequacy_report
        return get_adequacy_report()
    except Exception as e:
        print(f"[api] Error in get_adequacy: {e}")
        return {"error": str(e)}

