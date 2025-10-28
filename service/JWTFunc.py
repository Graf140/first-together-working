from functools import wraps

from jose import jwt
from jose.exceptions import *
import datetime
from config import jwt_config

class JWTFunctions:
    @staticmethod
    def generate_jwt_token(user_id:int, mail:str, phone:str):
        payload = {
            'user_id': user_id,
            'mail': mail,
            'phone':phone,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=jwt_config.get_time_expire()),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(
            payload,
            jwt_config.get_secret(),
            jwt_config.get_algorithm()
        )
        return token

    @staticmethod
    def take_token_info(token: str) -> dict | bool:
        try:
            payload = jwt.decode(
                token,
                jwt_config.get_secret(),
                algorithms=[jwt_config.get_algorithm()]
            )
            return payload
        except ExpiredSignatureError:
            print("Token error: expired")
            return False
        except JWTError as e:
            print("Token error:", e)
            return False

