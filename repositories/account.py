# Data Access Layer
import psycopg2.errors

from .db import get_db_connection, release_db_connection
from psycopg2 import DatabaseError
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation
from exceptions import *


class AccountRepository:
    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM accounts')
        users = cur.fetchall()
        cur.close()
        release_db_connection(conn)
        return users

    @staticmethod
    def get_users_count():
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('SELECT COUNT(*) FROM accounts')
            count = cur.fetchone()[0]
            return count
        finally:
            cur.close()
            release_db_connection(conn)

    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM accounts WHERE user_id = %s', (user_id,))
        user = cur.fetchone()
        cur.close()
        release_db_connection(conn)
        return user

    @staticmethod
    def get_user_by_email(email):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM accounts WHERE email = %s', (email,))
        user = cur.fetchone()
        cur.close()
        release_db_connection(conn)
        return user

    @staticmethod
    def get_user_by_phone(phone):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM accounts WHERE phone = %s', (phone,))
        user = cur.fetchone()
        cur.close()
        release_db_connection(conn)
        return user

    @staticmethod
    def create_account(first_name, last_name, email, middle_name, phone, avatar_url):
        conn = get_db_connection()
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("""
                    INSERT INTO accounts (email, phone, first_name, 
                                         middle_name, last_name, avatar_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                        """, (email, phone, first_name, middle_name, last_name, avatar_url))
            user_id = cur.fetchone()[0]
            conn.commit()
            return str(user_id)

        except DatabaseError: #не бизнес ошибка, не обрабатываем как кастомную
            conn.rollback()
            raise

        finally:
            if cur is not None:
                cur.close()
            release_db_connection(conn)