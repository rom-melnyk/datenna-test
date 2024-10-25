from fastapi import FastAPI
from . import db
from . import api

db.init()
app = FastAPI()

@app.get("/api/1.0/city/{city_id}")
async def get_city(city_id: int):
    return await api.get_city(city_id)

@app.get("/api/1.0/cities/{name_mask}")
async def get_cities(
    name_mask: str,
    # Query params:
    population_from: int = None,
    population_to: int = None
):
    return await api.get_cities(name_mask, population_from, population_to)

@app.get("/api/1.0/routes-from/{city_id}")
async def get_routes_from_city(
    city_id: int,
    # Query params:
    max_hops: int = None
):
    return await api.get_routes_from_city(city_id, max_hops)
