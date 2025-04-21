import jwt
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from passlib.context import CryptContext
from app.content.config import get_auth_data
from app.content.posts.dao import PostDAO
from app.content.posts.schemas import SPostResult

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token

async def get_available_post_by_id(user_id: int, post_id: int, check_author: bool = False) -> SPostResult:
    post = await PostDAO.find_one_or_none_by_id(post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пост не найден')
    if post.author_id != user_id and (post.is_private or check_author):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Пост не доступен')
    return post

async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')

    user = await UsersDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user