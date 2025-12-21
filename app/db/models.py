from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from .base import Base


class Portal(Base):
	__tablename__ = "portals"

	domain: Mapped[str] = mapped_column(String, primary_key=True)
	member_id: Mapped[str]

	token: Mapped["Token"] = relationship(
		back_populates="portal",
		uselist=False,
		cascade="all, delete-orphan",
		lazy="selectin"
	)


class Token(Base):
	__tablename__ = "tokens"

	id: Mapped[int] = mapped_column(primary_key=True)
	portal_domain: Mapped[str] = mapped_column(
		ForeignKey("portals.domain"),
		unique=True
	)

	access_token: Mapped[str]
	refresh_token: Mapped[str]

	portal: Mapped["Portal"] = relationship(
		back_populates="token",
		lazy="selectin"
	)
