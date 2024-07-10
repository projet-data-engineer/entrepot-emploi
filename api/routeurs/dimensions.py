from fastapi import APIRouter
import sys
sys.path.append('..')
from api.data.db import Db
from api.data.models import Rome

router = APIRouter()

_db = Db()

@router.get("/rome/", tags=["Dimensions"])
async def get_dim_rome() -> list[Rome]:
    return _db.get_dim_rome()
