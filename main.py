from fastapi import FastAPI

app = FastAPI()
print("Server started on port 8000...")
print("")
print("Possible calls:")
print("http://localhost:8000/")
print("GET: http://localhost:8000/hello/ic20b050")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}!"}
