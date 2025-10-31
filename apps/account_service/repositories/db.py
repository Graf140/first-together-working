# Data Access Layer
import psycopg2 #бд
from psycopg2 import pool

from config.database import DatabaseConfig


connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 1000,
    **DatabaseConfig.get_connection_parametres() #** для распаковки словаря
)


def get_db_connection():
    '''Подключение к postgress'''
    return connection_pool.getconn()


def release_db_connection(conn):
    '''Возвращаем подключение обратно в пул'''
    connection_pool.putconn(conn)