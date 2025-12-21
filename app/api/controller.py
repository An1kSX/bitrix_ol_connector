from fastapi import APIRouter, Request, HTTPException
from .service import APIService




router = APIRouter()
service = APIService()



@router.post("/install")
async def install(request: Request):
	try:
		auth = await service.parse_install(request)

		portal = await service.get_portal(auth.domain)

		await service.save_portal(portal)

		return {"status": "ok"}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
