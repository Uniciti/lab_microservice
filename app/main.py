# app/main.py
from fastapi import FastAPI
from database.connection import setup_database, get_db
from api.endpoints import router

app = FastAPI()

engine = setup_database()
database = get_db()

app.include_router(router)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)