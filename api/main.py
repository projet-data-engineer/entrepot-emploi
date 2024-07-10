from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data.db import Db
from routeurs import dimensions, geojson

_db = Db()

api = FastAPI(
    title='API Entrepôt emploi',
    description="Analyse des offres d'emploi de France Travail",
    version="1.0.1",
    openapi_tags=[
        {
            "name": "Dimensions",
            "description": "Table de dimensions de l'entrepôt de données"
        }
    ]
)

origins = [
    "http://localhost:3000"
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/geojson/regions/")
async def get_regions_geojson():
    return _db.get_regions_geojson()

#api.include_router(dimensions.router)
#api.include_router(geojson.router)