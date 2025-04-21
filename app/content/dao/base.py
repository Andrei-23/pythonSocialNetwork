from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from app.content.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def edit(cls, user_id, **values):
        async with async_session_maker() as session:
            async with session.begin():
                user = await session.get(cls.model, user_id)
                if user is None:
                    raise ValueError(f"User with id {user_id} not found")

                for key, value in values.items():
                    setattr(user, key, value)

                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return user

    @classmethod
    async def delete(cls, user_id):
        async with async_session_maker() as session:
            async with session.begin():
                user = await session.get(cls.model, user_id)
                if user is None:
                    raise ValueError(f"User with id {user_id} not found")

                await session.delete(user)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return user