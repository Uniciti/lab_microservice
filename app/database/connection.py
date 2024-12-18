# app/database/connection.py
import databases
import sqlalchemy
from config.database import DATABASE_URL, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from models.user import get_user_table

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)
users = get_user_table(metadata)

def setup_database():
    engine = sqlalchemy.create_engine(DATABASE_URL)
    
    try:
        metadata.create_all(engine)
        print("Таблицы успешно созданы!")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
    
    return engine

def get_db():
    return database