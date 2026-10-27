from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from .config import DB_URL

engine = create_engine(DB_URL,pool_pre_ping=True)

sessionLocal = sessionmaker(
    autoflush=False,
    autocommit = False,
    bind=engine,
    expire_on_commit=False
)

Base = declarative_base()

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

