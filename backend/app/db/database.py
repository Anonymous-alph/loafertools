from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool


DB_POOL_SIZE = 83
WEB_CONCURRENCY = 9
POOL_SIZE = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)

engine = create_async_engine(
    str(),
    echo = False,
    poolclass = AsyncAdaptedQueuePool,
    pool_size = POOL_SIZE,
    max_overflow = 10,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_ = AsyncSession,
    autoflush = False,
    autocommit = False,
    expire_on_commit = False,
)