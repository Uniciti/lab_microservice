# app/api/endpoints.py
from fastapi import APIRouter, HTTPException
from models.user import UserCreate, UserUpdate
from database.connection import database, users

router = APIRouter()

@router.post("/users/", response_model=dict)
async def create_user(user: UserCreate):
    try:
        query = users.insert().values(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            active=user.active
        )
        last_record_id = await database.execute(query)
        return {"id": last_record_id, **user.dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}")
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.get("/users/")
async def read_users():
    query = users.select()
    return await database.fetch_all(query)

@router.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    update_data = {k: v for k, v in user.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    query = users.update().where(users.c.id == user_id).values(update_data)
    await database.execute(query)
    
    select_query = users.select().where(users.c.id == user_id)
    result = await database.fetch_one(select_query)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}