from mypy.checker import is_private
from sqlalchemy import select
from app.content.database import async_session_maker

from app.content.dao.base import BaseDAO
from app.content.posts.models import Post

# class UsersDAO(BaseDAO):
#     model = User
#
#     @classmethod
#     async def find_one_or_none_by_id(cls, data_id: int):
#         async with async_session_maker() as session:
#             query = select(cls.model).filter_by(id=data_id)
#             result = await session.execute(query)
#             return result.scalar_one_or_none()
#
#     @classmethod
#     async def find_one_or_none(cls, login: str):
#         async with async_session_maker() as session:
#             query = select(cls.model).filter_by(login=login)
#             result = await session.execute(query)
#             return result.scalar_one_or_none()

class PostDAO(BaseDAO):
    model = Post

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_available_paginated(cls, count: int, first_post: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter(cls.model.is_private == False)
                .offset(first_post)
                .limit(count)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_user_posts(cls, user_id: int, public_only: bool = False):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter(cls.model.author_id == user_id and (not cls.model.is_private if public_only else True))
            )
            result = await session.execute(query)
            return result.scalars().all()