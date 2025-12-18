from pydantic import BaseModel




class BitrixAuth(BaseModel):
	access_token: str
	refresh_token: str
	expires_in: int
	domain: str
	member_id: str
