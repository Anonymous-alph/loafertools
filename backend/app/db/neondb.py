import os
import asyncio
import ssl
from sqlalchemy import text
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

load_dotenv()

def get_engine():
    url = settings.DATABASE_URL
    connect_args = {}
    
    # Handle SSL for asyncpg (Neon requires SSL)
    if "sslmode=" in url:
        url = url.replace("sslmode=require", "").replace("?sslmode=require", "").replace("&sslmode=require", "")
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        connect_args["ssl"] = ssl_context
    
    return create_async_engine(
        url,
        echo=True,
        pool_size=5,
        max_overflow=10,
        connect_args=connect_args,
    )

engine = get_engine()

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Optional: Function to test connection (call it from an endpoint, not here)
async def test_connection():
    async with engine.begin() as conn:
        print("Database connected successfully!")