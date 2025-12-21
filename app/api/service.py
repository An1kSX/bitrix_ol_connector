from fastapi import Request
from app.db import database
from app.db.models import *
from .models import *
from app.utils.logger import ModuleLogger


logger = ModuleLogger(__name__).get_logger()



class APIService:
	async def parse_install(self, request: Request) -> BitrixAuth:
		try:
			form = await request.form()

			return BitrixAuth(
				access_token=form["auth[access_token]"],
				refresh_token=form["auth[refresh_token]"],
				expires_in=int(form["auth[expires_in]"]),
				domain=form["auth[domain]"],
				member_id=form["auth[member_id]"],
			)

		except Exception as e:
			logger.error(f"Parse install error: {e}")
			raise

	async def get_portal(self, domain: str) -> Portal | None:
		try:
			portal = await database.get(Portal, domain)

			return portal

		except Exception as e:
			logger.error(f"Get portal error: {e}")
			raise

	async def save_portal(self, portal: Portal | None, auth: BitrixAuth) -> None:
		try:
			if portal:
				portal.member_id = auth.member_id

				if portal.token:
					portal.token.access_token = auth.access_token
					portal.token.refresh_token = auth.refresh_token
					
				else:
					portal.token = Token(
						access_token=auth.access_token,
						refresh_token=auth.refresh_token
					)
			else:
				portal = Portal(
					domain=auth.domain,
					member_id=auth.member_id,
					token=Token(
						access_token=auth.access_token,
						refresh_token=auth.refresh_token
					)
				)

			await database.save(portal)

		except Exception as e:
			logger.error(f"Save portal error: {e}")
			raise
