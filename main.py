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
print("POST: http://localhost:9000/addStrasse")
print(" HEADER: Content-Type: application/json")
print("	BODY: {\"skz\":108711,\"strassenname\":\"Andromedastraße\"}")
print("")
print("PUT: http://localhost:9000/changeStrasse/108711")
print("	HEADER: Content-Type: application/json")
print("	BODY: {\"strassenname\":\"Andromedastraße2\"}")
print("")
print("GET: http://localhost:9000/getStrasse?skz=108711")
print("")
print("DELETE: http://localhost:9000/deleteStrasse/108711")

pool = None


class JsonStrasse(BaseModel):
    skz: int | None = None  # optional parameter
    strassenname: str


@app.on_event("startup")
async def createPool():
    user = "postgres"
    password = "xsmmsgbAMfIOIWPPBrsc"
    host = "127.0.0.1"
    #host = "192.168.0.2"  # container ip
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

CREATE TABLE IF NOT EXISTS public.strasse
(
    skz integer NOT NULL,
    strassenname character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT strasse_pkey PRIMARY KEY (skz)
)""")
            return ""
    except Exception:
        traceback.print_exc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


# POST: http://localhost:9000/addStrasse
# HEADER: Content-Type: application/json
# BODY: {"skz":108711,"strassenname":"Andromedastraße"}
@app.post("/addStrasse", status_code=status.HTTP_201_CREATED)
async def addStrasse(strasse: JsonStrasse, response: Response):
    try:
        async with pool.acquire() as con:
            await con.execute(
                "INSERT INTO public.strasse(skz, strassenname) VALUES ($1, $2);", strasse.skz, strasse.strassenname)
            return ""
    except Exception:
        traceback.print_exc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


# PUT: http://localhost:9000/changeStrasse/108711
# HEADER: Content-Type: application/json
# BODY: {"strassenname":"Andromedastraße2"}
@app.put("/changeStrasse/{skz}")
async def changeStrasse(skz: int, strasse: JsonStrasse, response: Response):
    try:
        async with pool.acquire() as con:
            await con.execute(
                "UPDATE public.strasse SET strassenname=$1 WHERE skz=$2;", strasse.strassenname, skz)
            return ""
    except Exception:
        traceback.print_exc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


# GET: http://localhost:9000/getStrasse?skz=108711
@app.get("/getStrasse")
async def getStrasse(skz: int, response: Response):
    try:
        async with pool.acquire() as con:
            name = await con.fetchval(
                "SELECT strassenname FROM public.strasse WHERE skz=$1 LIMIT 1;", skz)
            if name is None:
                response.status_code = status.HTTP_404_NOT_FOUND
                return ""

            return {"skz": skz, "strassenname": name}
    except Exception:
        traceback.print_exc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


# DELETE: http://localhost:9000/deleteStrasse/108711
@app.delete("/deleteStrasse/{skz}")
async def deleteStrasse(skz: int, response: Response):
    try:
        async with pool.acquire() as con:
            await con.execute(
                "DELETE FROM public.strasse WHERE skz=$1;", skz)
            return ""
    except Exception:
        traceback.print_exc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
