from models.UserModel import UserModelActions
from models.UserSession import UserSessionModelActions
from werkzeug.security import check_password_hash
from service.JWTFunc import JWTFunctions
import datetime

#exceptions
# from exceptions.auth_exception import *

class AuthService:
    @staticmethod
    def authorize_user(mail:str, phone:str, password:str)-> str | None:
        user_data = UserModelActions.take_user(mail, phone)
        token = None
        if user_data["user_id"] is None:
            # raise AuthUserExists("User not found")
            print("ERROR: User not found")
            raise Exception
        if check_password_hash(user_data["password_hash"],password):
            try:
                token = JWTFunctions.generate_jwt_token(user_data["user_id"], user_data["mail"], user_data["phone"])
                UserSessionModelActions.new_session(token)
                UserSessionModelActions.change_status(token,True)
            except Exception as e:
                print("Error with token: ",e)
                return None
            return token
        else:
            # raise AuthInvalidCredentials("Incorrect password or username")
            print("ERROR: Incorrect password or username")
            raise Exception

    @staticmethod
    def change_user_status(jwt_token:str, status:bool) -> bool:
        try:
            result = UserSessionModelActions.change_status(jwt_token,status)
            if result:
                return True
            else:
                return False
        except Exception as e:
            print("ERROR: ",e)
            return False

    @staticmethod
    def check_token_session(token:str)->bool:
        status = None
        try:
            status = UserSessionModelActions.token_exists(token)
        except Exception as e:
            print("Error service: ",e)
            return False
        finally:
            return status

    @staticmethod
    def delete_user_session(token:str)->bool:
        status = None
        try:
            status = UserSessionModelActions.delete_session(token)
        except Exception as e:
            print("Error service: ",e)
            return False
        finally:
            return status




