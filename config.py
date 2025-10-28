from dotenv import load_dotenv
import os

load_dotenv()

class DatabaseConfig:
    def __init__(self):
        self.__db_name = os.getenv("PGDB")
        self.__db_user = os.getenv("PGUSER")
        self.__db_password = os.getenv("PGPASS")
        self.__db_host = os.getenv("PGHOST")
        self.__db_port = os.getenv("PGPORT")

    def get_config(self):
        return {
            "db_name": self.__db_name,
            "db_user": self.__db_user,
            "db_password": self.__db_password,
            "db_host": self.__db_host,
            "db_port": self.__db_port,
        }

    @staticmethod
    def get_pass()->str:
        return os.getenv("SECRET_KEY")

class JWTConfig:

    def __init__(self):
        self.__secret_key = os.getenv("SECRET_KEY")
        self.__time_expire_token = 15
        self.__crypt_algorithm = "HS256"

    def get_secret(self):
        return self.__secret_key

    def get_time_expire(self):
        return self.__time_expire_token

    def get_algorithm(self):
        return self.__crypt_algorithm

    def get_config(self):
        return {
            "secret":self.__secret_key,
            "time_expire":self.__time_expire_token,
            "algorithm":self.__crypt_algorithm
        }

class AccountServiceConnection:

    def __init__(self):
        self.__identification_factor = "1"
        self.__api_path_account = "/v1/accounts/load_data"

    def get_identification_factor(self):
        return self.__identification_factor

    def get_api_path_account(self):
        return self.__api_path_account

data =  DatabaseConfig()
jwt_config = JWTConfig()
account_service = AccountServiceConnection()