from fastapi import HTTPException
import os
from dotenv import load_dotenv

import grpc
from proto import main_service_pb2 as pb2
from proto import main_service_pb2_grpc as pb2_grpc


from app.interact.config import kafka_config

from fastapi import FastAPI

# router = APIRouter(prefix='/interact', tags=['Взаимодействие пользователя'])

# producer = Producer(kafka_config)

load_dotenv()
CORE_SERVICE_HOST = os.getenv("CORE_SERVICE_HOST", "localhost")
CORE_SERVICE_PORT = int(os.getenv("CORE_SERVICE_PORT", 50051))

app = FastAPI()

def get_grpc_client():
    channel = grpc.insecure_channel(f'{CORE_SERVICE_HOST}:{CORE_SERVICE_PORT}')
    return pb2_grpc.MainServiceStub(channel)

@app.post("/view_post")
async def view_post(post_id: int, user_id: int):
    client = get_grpc_client()
    request = pb2.PostEventRequest(post_id=post_id, user_id=user_id)
    response = client.ViewPost(request)
    if response.success:
        return {"message": response.message}
    raise HTTPException(status_code=500, detail="Failed to view post")

@app.post("/like_post")
async def like_post(post_id: int, user_id: int):
    client = get_grpc_client()
    request = pb2.PostEventRequest(post_id=post_id, user_id=user_id)
    response = client.LikePost(request)
    if response.success:
        return {"message": response.message}
    raise HTTPException(status_code=500, detail="Failed to like post")

@app.post("/comment_post")
async def comment_post(post_id: int, user_id: int, comment: str):
    client = get_grpc_client()
    request = pb2.CommentRequest(post_id=post_id, user_id=user_id, comment=comment)
    response = client.CommentPost(request)
    if response.success:
        return {"message": response.message}
    raise HTTPException(status_code=500, detail="Failed to add comment")

@app.get("/get_comments")
async def get_comments(post_id: int, page: int, page_size: int):
    client = get_grpc_client()
    request = pb2.GetCommentsRequest(post_id=post_id, page=page, page_size=page_size)
    response = client.GetComments(request)
    comments = [f"[{comment.timestamp}] {comment.comment}" for comment in response.comments]
    return {"comments": comments}

@app.post("/register_user")
async def register_user(user_id: int, username: str, reg_date: str):
    client = get_grpc_client()
    request = pb2.RegisterRequest(user_id=user_id, username=username, registration_date=reg_date)
    response = client.RegisterUser(request)
    if response.success:
        return {"user_id": response.user_id, "message": response.message}
    raise HTTPException(status_code=500, detail="Failed to save registration event")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)