from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from farfor_bot.api.dependencies import get_db


router = APIRouter()


@router.get("/ping")
def ping(db: Session = Depends(get_db)):
    db.execute("SELECT 1")

    return {"success": True}
