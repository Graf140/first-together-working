from models.database import get_db_action,close_db_action
from presentation.schemas.user import *
from presentation.schemas.user import PasswordHash
from pydantic import EmailStr


#id
#mail
#phone
#password_hash
#date_create

class UserModelActions:
    @staticmethod
    def reg_user(mail:str ,phone:str ,password_hash:str)->bool:
        connection = get_db_action()
        cursor = connection.cursor()
        status = None
        try:
            cursor.execute(
                "INSERT INTO users (mail, phone, password_hash) VALUES (%s, %s, %s) RETURNING id;",
                (mail, phone, password_hash)
            )
            result = cursor.fetchone()
            connection.commit()
            status = result is not None
        except Exception as e:
            print(e)
            connection.rollback()
        finally:
            cursor.close()
            close_db_action(connection)
            return status

    @staticmethod
    def delete_user(mail:str ,data:str)->bool:
        connection = get_db_action()
        cursor = connection.cursor()
        status = None
        try:
            cursor.execute(
                "DELETE FROM users WHERE mail=%s AND phone=%s;",
                (mail, data)
            )
            result = cursor.rowcount
            connection.commit()
            status = result > 0
        except Exception as e:
            print(e)
            connection.rollback()
        finally:
            cursor.close()
            close_db_action(connection)
            return status

    @staticmethod
    def take_pass(mail:str ,phone:str)-> PasswordHash | bool:
        connection = get_db_action()
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(
                "SELECT password_hash FROM users WHERE mail=%s AND phone=%s;",
                (mail, phone)
            )
            result = cursor.fetchone()[0]
            connection.commit()
            if result is None:
                return False
        except Exception as e:
            print(e)
            connection.rollback()
        finally:
            cursor.close()
            close_db_action(connection)
            return PasswordHash(password_hash=result)

    @staticmethod
    def take_user(mail:str, phone:str)-> UserOut | None:
        connection = get_db_action()
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(
                "SELECT * FROM users WHERE mail=%s AND phone=%s;",
                (mail, phone)
            )
            result = cursor.fetchone()
            connection.commit()
        except Exception as e:
            print(e)
            connection.rollback()
        finally:
            cursor.close()
            close_db_action(connection)
            if result is None:
                return result
            else:
                user_out = UserOut(
                    user_id=result[0],
                    mail=result[1],
                    phone=result[2],
                    password_hash=result[3],
                    date_created=result[4]
                )
                return user_out
