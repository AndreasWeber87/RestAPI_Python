# Sources:
# https://fastapi.tiangolo.com
# https://magicstack.github.io/asyncpg/current/index.html

from fastapi import FastAPI, status, Response
from pydantic import BaseModel
import traceback
import asyncpg

app = FastAPI()
print("Server started on port 9000...")
print("")
print("Possible calls:")
print("http://localhost:9000/")
print("Possible calls:")
print("GET: http://localhost:9000/")
print("")
print("POST: http://localhost:9000/createTable")
print("	BODY:")
print("")
print("POST: http://localhost:9000/addStreet")
print(" HEADER: Content-Type: application/json")
print("	BODY: {\"skz\":108711,\"streetname\":\"Andromedastraße\"}")
print("")
print("PUT: http://localhost:9000/changeStreet/108711")
print("	HEADER: Content-Type: application/json")
print("	BODY: {\"streetname\":\"Andromedastraße2\"}")
print("")
print("GET: http://localhost:9000/getStreet?skz=108711")
print("")
print("DELETE: http://localhost:9000/deleteStreet/108711")

pool = None


class JsonStreet(BaseModel):
    skz: int | None = None  # optional parameter
    streetname: str


@app.on_event("startup")
async def createPool():
    user = "postgres"
    password = "xsmmsgbAMfIOIWPPBrsc"
    host = "192.168.0.2"
    port = "5432"
    database = "ogd"

    global pool
    pool = await asyncpg.create_pool(f'postgresql://{user}:{password}@{host}:{port}/{database}')


# GET: http://localhost:9000/
@app.get("/")
async def home():
    return {"message": "Hello World! I'm the Python API."}


# POST: http://localhost:9000/createTable
# BODY:
@app.post("/createTable", status_code=status.HTTP_201_CREATED)
async def createTable(response: Response):
    try:
        async with pool.acquire() as con:
            await con.execute(
                """DROP TABLE IF EXISTS public.strasse;

CREATE TABLE public.strasse
(
    skz integer NOT NULL,
    strassenname character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT strasse_pkey PRIMARY KEY (skz)
)""")
            return {"message": "Table created successfully."}
    except Exception:
        traceback.print_exc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


# POST: http://localhost:9000/addStreet
# HEADER: Content-Type: application/json
# BODY: {"skz":108711,"streetname":"Andromedastraße"}
@app.post("/addStreet", status_code=status.HTTP_201_CREATED)
async def addStreet(street: JsonStreet, response: Response):
    try:
        async with pool.acquire() as con:
            await con.execute(
                "INSERT INTO public.strasse(skz, strassenname) VALUES ($1, $2);", street.skz, street.streetname)
            return {"message": "Street added successfully."}
    except Exception:
        traceback.print_exc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


# PUT: http://localhost:9000/changeStreet/108711
# HEADER: Content-Type: application/json
# BODY: {"streetname":"Andromedastraße2"}
@app.put("/changeStreet/{skz}")
async def changeStreet(skz: int, street: JsonStreet, response: Response):
    try:
        async with pool.acquire() as con:
            res = await con.execute(
                "UPDATE public.strasse SET strassenname=$1 WHERE skz=$2;", street.streetname, skz)
            if res == "UPDATE 0":
                return {"message": "ID not found."}
            return {"message": "Street changed successfully."}
    except Exception:
        traceback.print_exc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


# GET: http://localhost:9000/getStreet?skz=108711
@app.get("/getStreet")
async def getStreet(skz: int, response: Response):
    try:
        async with pool.acquire() as con:
            name = await con.fetchval(
                "SELECT strassenname FROM public.strasse WHERE skz=$1 LIMIT 1;", skz)
            if name is None:
                return {"message": "No street found."}

            return {"skz": skz, "streetname": name}
    except Exception:
        traceback.print_exc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


# DELETE: http://localhost:9000/deleteStreet/108711
@app.delete("/deleteStreet/{skz}")
async def deleteStreet(skz: int, response: Response):
    try:
        async with pool.acquire() as con:
            await con.execute(
                "DELETE FROM public.strasse WHERE skz=$1;", skz)
            return {"message": "Street deleted successfully."}
    except Exception:
        traceback.print_exc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
