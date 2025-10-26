from models.database import get_db_action,close_db_action

#id
#mail
#phone
#password_hash
#date_create

class UserModelActions:
    @staticmethod
    def reg_user(mail:str , phone:str, password_hash:str)->bool:
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
    def delete_user(**kwargs)->bool:
        connection = get_db_action()
        cursor = connection.cursor()
        status = None
        mail = kwargs.get('mail')
        phone = kwargs.get('phone')
        if not mail or not phone:
            return False
        try:
            cursor.execute(
                "DELETE FROM users WHERE mail=%s AND phone=%s;",
                (mail, phone)
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
    def take_pass(**kwargs)->str | bool:
        connection = get_db_action()
        cursor = connection.cursor()
        result = None
        mail = kwargs.get('mail')
        phone = kwargs.get('phone')
        if not mail or not phone:
            return False
        try:
            cursor.execute(
                "SELECT password_hash FROM users WHERE mail=%s AND phone=%s;",
                (mail,phone)
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
            return result

    @staticmethod
    def take_user(mail:str , phone:str)-> dict | None:
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
                return {
                    "user_id":result[0],
                    "mail":result[1],
                    "phone":result[2],
                    "password_hash":result[3],
                    "date_created":result[4]
                }

# print(UserModelActions.take_pass(mail="penis@gmail.com",phone="79103568252"))
# print(UserModelActions.delete_user(mail="penis@gmail.com",phone="79103568252"))

#import json
# from typing import Any
#
# from models.database import get_db_action,close_db_action
# class UserDataActions:
#
#     @staticmethod
#     def create_user(login, password)-> bool:
#         flag = False
#         connection = get_db_action()
#         cursor = connection.cursor()
#         try:
#             cursor.execute(
#                 "INSERT INTO users (user_login, password_hash) VALUES (%s, %s);",
#                 (login, password)
#             )
#             connection.commit()
#             flag = True
#         except Exception as e:
#             print("CREATE USER: ",e)
#             return False
#         finally:
#             cursor.close()
#             close_db_action(connection)
#             return flag
#
#     @staticmethod
#     def delete_user(login)-> bool:
#         flag = False
#         connection = get_db_action()
#         cursor = connection.cursor()
#         try:
#             cursor.execute(
#                 "DELETE FROM users WHERE user_login = %s;",
#                 (login,)
#                )
#             connection.commit()
#             flag = True
#         except Exception as e:
#             print("DELETE USER: ",e)
#         finally:
#             cursor.close()
#             close_db_action(connection)
#             return flag
#
#     @staticmethod
#     def get_user(login):
#         connection = get_db_action()
#         cursor = connection.cursor()
#         try:
#             cursor.execute("SELECT * FROM users WHERE user_login = %s", (login,))
#             result = cursor.fetchone()
#             if result is None:
#                 return None
#             return {
#                 "user_id": result[0],
#                 "user_login": result[1],
#                 "user_pass": result[2],
#                 "user_date_create": result[3]
#             }
#         except Exception as e:
#             print("GET USER:", e)
#             return None
#         finally:
#             cursor.close()
#             close_db_action(connection)
#
#     @staticmethod
#     def take_password(username:str)->str:
#         result = None
#         connection = get_db_action()
#         cursor = connection.cursor()
#         try:
#             cursor.execute(
#                 "SELECT password_hash FROM users WHERE user_login = %s",
#                 (username,)
#             )
#             connection.commit()
#             result = cursor.fetchone()
#         except Exception as e:
#             print("GET USER: ", e)
#         finally:
#             cursor.close()
#             close_db_action(connection)
#             if result:
#                 return result
#             else:
#                 return False
#
#     @staticmethod
#     def add_true_token(username:str, token:str)->bool:
#         flag = False
#         connection = get_db_action()
#         cursor = connection.cursor()
#         try:
#             cursor.execute(
#                 "INSERT INTO user_session (username, token) VALUES (%s, %s);",
#                 (username, token)
#             )
#             connection.commit()
#             flag = True
#         except Exception as e:
#             print("ERROR TOKEN: ", e)
#         finally:
#             cursor.close()
#             close_db_action(connection)
#             return flag
#
#     @staticmethod
#     def take_token(username:str)-> dict[str, Any] | None:
#         token = None
#         connection = get_db_action()
#         cursor = connection.cursor()
#         try:
#             cursor.execute(
#                 "SELECT token,date_session FROM user_session WHERE username=%s;",
#                 (username,)
#             )
#             connection.commit()
#             info = cursor.fetchone()
#             token = {
#                 "token":info[0],
#                 "date":info[1]
#             }
#         except Exception as e:
#             print("ERROR TAKE TOKEN: ", e)
#         finally:
#             cursor.close()
#             close_db_action(connection)
#             return token
#
#     @staticmethod
#     def delete_token(username: str, token: str) -> bool:
#         connection = get_db_action()
#         cursor = connection.cursor()
#         try:
#             cursor.execute(
#                 "DELETE FROM user_session WHERE username = %s AND token = %s;",
#                 (username, token)
#             )
#             connection.commit()
#             return cursor.rowcount > 0
#         except Exception as e:
#             print("ERROR DELETE TOKEN:", e)
#             connection.rollback()
#             return False
#         finally:
#             cursor.close()
#             close_db_action(connection)
#
#     @staticmethod
#     def get_users():
#         connection = get_db_action()
#         cursor = connection.cursor()
#         data = None
#         try:
#             cursor.execute(
#                 "SELECT * FROM users"
#             )
#             connection.commit()
#             data = cursor.fetchall()
#         except:
#             print("ERROR GET USERS")
#         finally:
#             return data

# print(UserDataActions.add_true_token("admin","asdasdasd"))
# print(UserDataActions.delete_token("admin"))
# print(UserDataActions.take_token("admin"))

