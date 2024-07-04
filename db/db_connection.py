from pydantic_settings import BaseSettings
from pydantic import Field
import pymysql

class Settings(BaseSettings):
    db_host: str = 'localhost'
    db_port: int = 3306
    db_name: str = 'cog'
    db_user: str = 'root'
    db_password: str = ''

def db_connect():
    settings = Settings()
    try:
        connection = pymysql.connect(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password,
            database=settings.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print(f"Error: {e}")
        return None
