from fastapi import APIRouter, Request
from .service import APIService




router = APIRouter()
service = APIService()



@router.post("/install")
async def install(request: Request):
	auth = await service.parse_install(request)

	portal = await service.get_portal(auth.domain)

	await service.save_portal(portal)

	return {"status": "ok"}
