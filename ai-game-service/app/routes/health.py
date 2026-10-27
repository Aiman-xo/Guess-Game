from fastapi import APIRouter,Depends,HTTPException
from app.core.database import Base,get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix='/health',tags=['health'])

@router.get('')
def db_liveness():
    return {"status":'ok'}

@router.get('/ready')
def db_readiness(db:Session = Depends(get_db)):
    try:
        db.execute(text("select 1"))
    except SQLAlchemyError:
        raise HTTPException(status_code=503, detail="database unavailable")
    return {"status": "ready", "database": "ok"}