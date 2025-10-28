from models.UserModel import UserModelActions
from models.UserSession import UserSessionModelActions
from werkzeug.security import check_password_hash
from service.JWTFunc import JWTFunctions
import datetime
from presentation.schemas.auth import *
from presentation.Exceptions.AuthExceptions import *



class AuthService:
    @staticmethod
    def authorize_user(data: LoginRequest)-> str | None:
        user_data = UserModelActions.take_user(data.mail, data.phone)
        token = None
        if user_data is None:
            raise AuthServiceUserExists("User already exists")
        if check_password_hash(user_data.password_hash,data.password):
            try:
                token = JWTFunctions.generate_jwt_token(user_data.user_id, user_data.mail, user_data.phone)
                UserSessionModelActions.new_session(token)
                UserSessionModelActions.change_status(token=token,status=True)
            except Exception as e:
                raise AuthServiceTokenError("Wrong token")
            return token
        else:
            raise AuthServiceWrongCredit("Incorrect password or username")

    @staticmethod
    def change_user_status(data: SessionStatusUpdate) -> bool:
        try:
            result = UserSessionModelActions.change_status(
                token=data.token,
                status=data.status
            )
            if result:
                return True
            else:
                return False
        except Exception as e:
            raise AuthServiceDeeperFail("Something went wrong on models layer: ",e)

    @staticmethod
    def check_token_session(data: TokenRequest)->bool:
        status = None
        try:
            status = UserSessionModelActions.token_exists(data.token)
        except Exception as e:
            raise AuthServiceDeeperFail("Something went wrong on models layer: ",e)
        finally:
            return status

    @staticmethod
    def delete_user_session(data: TokenRequest)->bool:
        status = None
        try:
            status = UserSessionModelActions.delete_session(data.token)
        except Exception as e:
            raise AuthServiceDeeperFail("Something went wrong on models layer: ",e)
        finally:
            return status




