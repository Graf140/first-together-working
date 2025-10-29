from models.UserModel import UserModelActions
from werkzeug.security import generate_password_hash
from presentation.Exceptions.RegistrationExceptions import *


class RegistrationMethods:
    @staticmethod
    def registrate_user(mail:str, phone:str, password:str)->int | bool:
        hashed_pass = generate_password_hash(password=password, method="scrypt", salt_length=16)
        if UserModelActions.take_user(mail,phone) is not None:
            raise RegistrationServiceUserExists("User already exists")
        try:
            status = UserModelActions.reg_user(
                mail=mail,
                phone=phone,
                password_hash=hashed_pass
            )
            return status
        except Exception as e:
            raise RegistrationServiceDeeperFail("Something went wrong on models layer: ",e)

