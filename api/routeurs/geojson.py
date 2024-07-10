from fastapi import APIRouter
import sys
sys.path.append('..')
from api.data.db import Db

router = APIRouter()

_db = Db()

@router.get("/regions/")
async def get_regions_geojson():
    return "ghghg"