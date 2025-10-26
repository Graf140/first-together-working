import psycopg2
from psycopg2 import pool

from config import DatabaseConfig

database_config = DatabaseConfig()

connect_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,maxconn=20,
    user=database_config.get_config().get("db_user"),
    password=database_config.get_config().get("db_password"),
    database=database_config.get_config().get("db_name"),
    host=database_config.get_config().get("db_host"),
    port=database_config.get_config().get("db_port")
)

def get_db_action():
    try:
        return connect_pool.getconn()
    except:
        raise Exception("Pool init error")

def close_db_action(simple_pool)->None:
    try:
        connect_pool.putconn(simple_pool)
    except:
        raise Exception("Pool close error")
