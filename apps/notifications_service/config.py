import os
from dotenv import load_dotenv

load_dotenv()

class MailConfig:
    '''Загружаем из конфига данные в программу(так называемая безопасная загрузка)'''
    mail_address = os.getenv("MAIL_ADDRESS")
    mail_port = os.getenv("MAIL_PORT")
    mail_host = os.getenv("MAIL_HOST")
    

    @classmethod
    def get_connection_parametres(cls) -> object:
        return {
            "mail_address": cls.mail_address,
            "mail_port": cls.mail_port,
            "mail_host": cls.mail_host
        }