import re
from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict, field_validator, EmailStr
from typing_extensions import Optional


# def validate_phone(phone_number: str):
#     if not re.match(r'^\+\d{1,15}$', phone_number):
#         raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
#     return phone_number
#
class SPostData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    is_private: bool
    tags: list[str]

class SPostResult(SPostData):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int

    created_at: datetime
    updated_at: datetime


# class SUserRegister(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     login: str = Field(..., min_length=5, max_length=50, description="Логин пользователя, от 5 до 50 знаков")
#     password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
#     email: EmailStr = Field(..., description="Электронная почта")
#     phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
#     first_name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
#     last_name: str = Field(..., min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")
#
#     @field_validator("phone_number")
#     def validate_phone_number(cls, value: str) -> str:
#         return validate_phone(value)
#
# class SUserAuth(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     login: str = Field(..., min_length=5, max_length=50, description="Логин пользователя, от 5 до 50 знаков")
#     password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
#
# class SUserEdit(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     email: EmailStr = Field(..., description="Электронная почта (обязательно)")
#     phone_number: Optional[str] = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
#     first_name: Optional[str] = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
#     last_name: Optional[str] = Field(..., min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")
#     date_of_birth: Optional[date] = Field(..., description="Дата рождения")
#
#     @field_validator("phone_number")
#     def validate_phone_number(cls, value: Optional[str]) -> Optional[str]:
#         if value is None:
#             return value
#         return validate_phone(value)
