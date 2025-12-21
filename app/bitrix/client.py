from fast_bitrix24 import BitrixAsync
from app.db import models
from app.db.database import db
from fast_bitrix24 import BitrixAsync
import os
import httpx


BITRIX_CLIENT_ID = os.getenv("BITRIX_CLIENT_ID")
BITRIX_CLIENT_SECRET = os.getenv("BITRIX_CLIENT_SECRET")
BITRIX_OAUTH_URL = "https://oauth.bitrix.info/oauth/token"



class BitrixClient:
	def __init__(self, portal: models.Portal):
		self.portal = portal
		self.client = BitrixAsync(
			portal=f"https://{portal.domain}",
			token=self.portal.token.access_token,
			token_func=self._token_func
		)

	async def _token_func(self) -> str:
		data = await self.refresh_token(
			BITRIX_CLIENT_ID,
			BITRIX_CLIENT_SECRET,
			self.portal.token.refresh_token
		)

		self.portal.token.access_token = data["access_token"]
		self.portal.token.refresh_token = data["refresh_token"]

		await db.save(self.portal)

		return self.portal.token.access_token

	async def refresh_token(
		self,
		client_id: str,
		client_secret: str,
		refresh_token: str
	) -> dict:
		async with httpx.AsyncClient(timeout=10) as client:
			resp = await client.get(
				BITRIX_OAUTH_URL,
				params={
					"grant_type": "refresh_token",
					"client_id": client_id,
					"client_secret": client_secret,
					"refresh_token": refresh_token,
				}
			)

		resp.raise_for_status()
		return resp.json()
