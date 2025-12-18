from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os



user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
dbname = os.getenv("POSTGRES_DBNAME")
host = os.getenv("POSTGRES_HOST")
port = int(os.getenv("POSTGRES_PORT", "5433"))


DATABASE_URL = (
		f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"
	)

engine = create_async_engine(
	DATABASE_URL,
	echo=False
)

SessionFactory = async_sessionmaker(
	engine,
	expire_on_commit=False
)
