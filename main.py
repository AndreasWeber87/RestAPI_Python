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

conn = None

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
        global conn

        if conn is None:
            user = "postgres"
            password = "xsmmsgbAMfIOIWPPBrsc"
            host = "127.0.0.1"
            # host = "192.168.0.2"  # container ip
            port = "5432"
            database = "ogd"
            conn = await asyncpg.connect(f'postgresql://{user}:{password}@{host}:{port}/{database}')

        row = await conn.fetchrow(
            'SELECT gemeindename FROM public.gemeinde WHERE gkz=$1 LIMIT 1', id)
        # await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"gemeindename": row}
