from typing import Type, TypeVar, Sequence
from sqlalchemy import select
from .session import SessionFactory
from .base import Base
from . import models

T = TypeVar("T", bound=Base)

class Database:
	def __init__(self):
		self._session_factory = SessionFactory

	@staticmethod
	async def init_db():
		async with engine.begin() as conn:
			await conn.run_sync(Base.metadata.create_all)

	async def get(self, model: Type[T], pk) -> T | None:
		async with self._session_factory() as session:
			return await session.get(model, pk)

	async def save(self, obj: T) -> T:
		async with self._session_factory() as session:
			session.add(obj)
			await session.commit()
			return obj

	async def delete(self, obj: T):
		async with self._session_factory() as session:
			await session.delete(obj)
			await session.commit()

	async def filter(
		self,
		model: Type[T],
		*conditions
	) -> Sequence[T]:
		async with self._session_factory() as session:
			stmt = select(model)
			if conditions:
				stmt = stmt.where(*conditions)
			result = await session.execute(stmt)
			return result.scalars().all()
