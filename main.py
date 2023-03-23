# Sources:
# https://fastapi.tiangolo.com
# https://magicstack.github.io/asyncpg/current/index.html

from fastapi import FastAPI, HTTPException
import asyncpg

app = FastAPI()
print("Server started on port 9000...")
print("")
print("Possible calls:")
print("http://localhost:9000/")
print("GET: http://localhost:9000/hello/ic20b050")
print("POST: http://localhost:9000/hello/name  name=ic20b050")
print("")
print("GET: http://localhost:9000/getGemeinde?id=10101")

pool = None


async def createPool():
    user = "postgres"
    password = "xsmmsgbAMfIOIWPPBrsc"
    #host = "127.0.0.1"
    host = "192.168.0.2"  # container ip
    port = "5432"
    database = "ogd"

    global pool
    #pool = await asyncpg.create_pool(user='postgres', host='127.0.0.1')
    pool = await asyncpg.create_pool(f'postgresql://{user}:{password}@{host}:{port}/{database}')

@app.get("/")
async def root():
    return {"message": "Hello World! I'm the FastAPI in Python."}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}! I'm the FastAPI in Python."}


@app.post("/hello/{name}")
async def create_item(name: str):
    return {"message": f"Hello {name}! I'm the FastAPI in Python."}


@app.get("/getGemeinde")
async def say_hello(id: int):
    try:
        if pool is None:
            await createPool()

        async with pool.acquire() as con:
            row = await con.fetchrow(
                'SELECT gemeindename FROM public.gemeinde WHERE gkz=$1 LIMIT 1', id)
            return {"gemeindename": row}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
