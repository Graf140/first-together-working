from config import account_service
from presentation.schemas.post_account import PostAccount
import requests


def post_data_to_accounts(data: PostAccount):
    json_data = {
        "user_id": data.user_id,
        "first_name": data.first_name,
        "middle_name": data.middle_name,
        "last_name": data.last_name,
        "email": data.mail,
        "phone": data.phone,
        "token": account_service.get_identification_factor()
    }
    api_path = account_service.get_api_path_account()
    response = requests.post(api_path, json=json_data)
    if response.status_code != 200:
        print("post error: ",response.status_code)
