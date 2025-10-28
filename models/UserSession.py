from models.database import get_db_action, close_db_action
from presentation.schemas.session import *


class UserSessionModelActions:
    @staticmethod
    def new_session(token:str)->bool:
        connection = get_db_action()
        cursor = connection.cursor()
        status = None
        try:
            cursor.execute(
                "INSERT INTO user_session (token) VALUES (%s) RETURNING id;",
                (token,)
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
    def token_exists(token:str) -> bool:
        connection = get_db_action()
        cursor = connection.cursor()
        status = None
        try:
            cursor.execute(
                "SELECT * FROM user_session WHERE token=%s;",
                (token,)
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
    def change_status(status:bool, token:str)->bool:
        connection = get_db_action()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE user_session SET status=%s WHERE token=%s;",
                (status, token)
            )
            result = cursor.rowcount
            connection.commit()
            status = result>0
        except Exception as e:
            print(e)
            connection.rollback()
        finally:
            cursor.close()
            close_db_action(connection)
            return status

    @staticmethod
    def delete_session(token:str) -> bool:
        connection = get_db_action()
        cursor = connection.cursor()
        status = None
        try:
            cursor.execute(
                "DELETE FROM user_session WHERE token=%s;",
                (token,)
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
    def update_token(new_token:str, true_token:str)->bool:
        connection = get_db_action()
        cursor = connection.cursor()
        status = None
        try:
            cursor.execute(
                "UPDATE user_session SET token=%s WHERE token=%s;",
                (new_token, true_token)
            )
            result = cursor.rowcount
            connection.commit()
            status = result>0
        except Exception as e:
            print(e)
            connection.rollback()
        finally:
            cursor.close()
            close_db_action(connection)
            return status