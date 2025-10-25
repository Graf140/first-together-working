from fastapi import FastAPI, HTTPException
from repositories.acount import AcountRepository


class AcountService:
    @staticmethod
    def create_or_update_user(first_name, last_name, email, midle_name, user_id, phone):
        # Проверка на дубликаты
        if AcountRepository.get_user_by_email(email) is not None:
            raise HTTPException(status_code=409, detail="Email already exists")
        if AcountRepository.get_user_by_phone(phone) is not None:
            raise HTTPException(status_code=409, detail="Phone already exists")

        AcountRepository.create_user(
            email=email,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            midle_name=midle_name,
            user_id=user_id
        )

        return {"Success": True}
