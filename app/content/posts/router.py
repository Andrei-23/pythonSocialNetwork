import time

from fastapi import APIRouter, Depends, Path, HTTPException, status, Response

from app.content.posts.models import Post
from app.content.posts.dao import PostDAO
from app.content.posts.schemas import SPostData, SPostResult
from app.content.posts.post_functions import get_available_post_by_id

router = APIRouter(prefix='/posts', tags=['Работа с постами'])


@router.get("/feed", summary="Получить все доступные посты в пагинированном формате")
async def get_available_posts(count: int, first_post: int) -> list[SPostResult]:
    return await PostDAO.find_available_paginated(count, first_post)

@router.get("/get_post", summary="Получить пост по id")
async def get_post_by_id(user_id: int, post_id: int) -> SPostResult:
    return await get_available_post_by_id(user_id, post_id)

@router.get("/get_all_user_posts", summary="Получить все посты пользователя")
async def get_all_posts_by_id(user_id: int) -> list[SPostResult]:
    return await PostDAO.find_user_posts(user_id, False)

@router.get("/get_public_user_posts", summary="Получить публичные посты пользователя")
async def get_public_posts_by_id(user_id: int) -> list[SPostResult]:
    return await PostDAO.find_user_posts(user_id, True)

@router.post("/create_post", summary="Создать пост")
async def create_post(user_id: int, post_data: SPostData) -> dict:
    post_dict = post_data.dict()
    post_dict["author_id"] = user_id
    await PostDAO.add(**post_dict)
    return {'message': 'Пост создан'}

@router.post("/edit_post", summary="Редактировать пост")
async def edit(user_id: int, post_id: int, post_data: SPostData) -> SPostResult:
    _ = await get_available_post_by_id(user_id, post_id, True)
    post_dict = post_data.dict()
    await PostDAO.edit(post_id, **post_dict)
    return await get_available_post_by_id(user_id, post_id, True)

@router.delete("/delete_post", summary="Удалить пост")
async def create_post(user_id: int, post_id: int) -> dict:
    _ = await get_available_post_by_id(user_id, post_id, True)
    await PostDAO.delete(post_id)
    return {'message': 'Пост удалён'}
