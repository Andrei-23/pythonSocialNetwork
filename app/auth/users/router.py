from fastapi import APIRouter, Depends, Path, HTTPException, status, Response

from app.auth.users.models import User
from app.auth.users.dao import UsersDAO
from app.auth.users.schemas import SUser, SUserRegister, SUserAuth, SUserEdit

from app.auth.users.auth import get_password_hash, create_access_token, get_current_user
from app.auth.users.auth import authenticate_user

router = APIRouter(prefix='/users', tags=['Работа с пользователями'])

# @router.get("/", summary="Получить всех пользователей")
# async def get_all_students(request_body: RBUser = Depends()) -> list[SUser]:
#     return await UsersDAO.find_all(**request_body.to_dict())

@router.get("/{login}", summary="Получить пользователя по id")
async def get_user_by_id(login: str = Path(...)) -> SUser | dict:
    print("ok")
    res = await UsersDAO.find_one_or_none(login=login)
    if res is None:
        return {'message': f'Пользователь {login} не найден.'}
    return res

@router.post("/register/", summary="Регистрация пользователя")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(login=user_data.login)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}

@router.post("/login/")
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(password=user_data.password, login=user_data.login)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}

@router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data

@router.post("/edit-user/")
async def edit_user(new_data: SUserEdit, user_data: User = Depends(get_current_user)):
    user_dict = new_data.dict()
    await UsersDAO.edit(user_data.id, **user_dict)
    return {'message': 'Данные обновлены'}


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}

