# Datenna Test Assignment



## Background

A RESTful API that demostrates simple graph data manipulations. It's possible to:
- get the node info,
- search the nodes by given criteria,
- add the nodes and the edges,
- get related nodes (recommendations).



## Legend / Data domain

In 2052 we established link with the first inhabited planet around 20 light years away.
It seems that they have a pretty developed transport system between their cities.

The app data is based on the alien transport grid:
- **Nodes** correspond to the cities.
  A node has 2 props: `name: str` and `population: int(>=1k, <=1M)`.
- **Edges** correspond to the transport connections between the cities.
  An edge has one extra property: `distance: int | float`.

### ⚙️ Technical

The data is auto-generated (if missing) during first app startup (check the `db.init()`).
The data is stored in the `.sample_data.py` file (check the `graph.sample_data` module).
The file is loaded upon all the subsequent app (re)starts.

The in-memory graph representation is used (check the `graph.*` modules).
This is done for the sake of demostration and know flaws are accepted.
The real graph DB (e.g., Neo4J) can be used; check the implementation of the `db.py` and the `api.py`.

> **⚠️ Important**
> 1. The data (city names, routes and props) is generated randomly.
>    Hence, after deleting the `.sample_data.graph`, the app restarts
>    with brand-new cities and routes.
> 1. The user-generated content is not persisted,
>    so it _does not survive the server restart!_



## API

Consider the app is running on the `http://127.0.0.1:8000`.


### `GET /api/1.0/cities`

**Returns** the list of the cities (nodes) by given criteria.

**Query params:**
- `name`: optional; a name mask (case-insensitive; allows the `*` wildcard):
   - `?name=ast` matches the "last", "Astra" but doesn't match the "La-St".
   - `?name=a*t` matches the "last", "Assertion" but doesn't match the "Assembly".
- `ppl_over` and `ppl_under`: both optional; limit the output by the population.

**Examples:**
```
GET /api/1.0/cities?name=ab*c
GET /api/1.0/cities?ppl_over=250000&ppl_under=500000
GET /api/1.0/cities?name=ab*&ppl_over=750000
```

**🐞 Known issues:**
The output would benefit from the pagination
(because `GET /api/1.0/cities` without query params returns 10k records).


### `GET /api/1.0/city/{city_id}`

**Returns** the city (node) info if found.

**Examples:**
```
GET /api/1.0/city/555
    ⬇️ 200 / { "id": 555, "props": { "name": "...", "population": ... } }
GET /api/1.0/city/123456789
    ⬇️ 404 / { "error": true }
```


### `POST /api/1.0/city`

**Adds** the city to the database.
**Returns** the added city node.

**Body type and structure:** JSON / `{ "name": str, "population": int }`

**Examples:**
```
POST /api/1.0/cities?name=ab*c
     ⬆️ Content-Type: application/json
     ⬆️ { "name": "New York", "population": 15000000 }

     ⬇️ // Same as the city/node output
```

**⚠️ Known limitations:** It's not permitted to create the city with existing name.


### `GET /api/1.0/routes-from/{city_id}`

**Returns** the list of the routes from given city.
Consider this as _recommendations_ for the city:
- The routes contain the destination (think _"recommended"_) cities.
- The routes are ordered by travel convenience:
  first by number or stopovers (direct routes first),
  then by distance (closest first within same stopover group).

**Query params:**
- `max_hops`: optional; set to `2` if omitted.
  Defines the max route length (1 → direct routes; 3 → with two stopovers).
  Must be within [1..3] because it makes little sense to travel with 3+ stopovers.

**Examples:**
```
GET /api/1.0/routes-from/555
GET /api/1.0/routes-from/555?max_hops=1
```

**Errors** (400 / `{ "error": true }`) are returned in case of unknown city id
or if `max_hops` is out of fange.


### `POST /api/1.0/route`

**Adds** the route to the database.
**Returns** the added route edge.

**Body type and structure:** JSON / `{ "from_id": int, "to_id": int, "distance": int | float }`

**Examples:**
```
POST /api/1.0/route
     ⬆️ Content-Type: application/json
     ⬆️ { "from_id": 1, "to_id": 555, "distance": 15000 }

     ⬇️ // Edge object
```

**Errors** (400 / `{ "error": true }`) are returned in case of unknown `from`/`to` city ids.


## Installation

1. Prerequisites:
   - Python v3.10+.
   - `pip` installed.
   - `fastapi` installed (follow the [instructions](https://fastapi.tiangolo.com/#installation)).
1. Run `fastapi run main.py`.
1. Access the API at `http://127.0.0.1:8000/api/1.0/*` (check the API section)
