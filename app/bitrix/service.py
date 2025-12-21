from app.db import database
from app.db.models import *
from .client import Bitrix




class BitrixService:
	def __init__(self, domain: str):
		self.domain = domain
		self.bx24 = None

	async def _get_client(self):
		if not self.bx24:
			portal = await database.get(Portal, self.domain)

			if not portal or not portal.token:
				raise RuntimeError("Portal not installed")

			self.bx24 = Bitrix(portal)

		return self.bx24.client

	async def get_users(self):
		client = await self._get_client()
		method = "user.get"
		params = {}

		return await client.call(method, params)
