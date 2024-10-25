from fastapi import FastAPI, Response
from . import db
from . import api

db.init()
app = FastAPI()

@app.get("/api/1.0/city/{city_id}")
async def get_city(city_id: int, response: Response):
    return await api.get_city(city_id, response)

@app.post("/api/1.0/city")
async def add_city(city: api.City, response: Response):
    return await api.add_city(city, response)

@app.get("/api/1.0/cities")
async def get_cities(
    response: Response,
    # Query params:
    name: str = None,
    ppl_over: int = None,
    ppl_under: int = None,
):
    return await api.get_cities(name, ppl_over, ppl_under, response)

@app.get("/api/1.0/routes-from/{city_id}")
async def get_routes_from_city(
    city_id: int,
    response: Response,
    # Query params:
    max_hops: int = None,
):
    return await api.get_routes_from_city(city_id, max_hops, response)

@app.post("/api/1.0/route")
async def add_route(route: api.Route, response: Response):
    return await api.add_route(route, response)
