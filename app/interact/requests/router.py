import time

from confluent_kafka import Producer
from fastapi import APIRouter, Depends, Path, HTTPException, status, Response
import datetime
import json

from app.interact.requests.models import UserRegisterInfo, InteractionData, CommentData
from app.interact.config import kafka_config


router = APIRouter(prefix='/interact', tags=['Взаимодействие пользователя'])

producer = Producer(kafka_config)

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def send_to_kafka(topic: str, message: dict):
    try:
        producer.produce(topic, key=str(datetime.datetime.now().timestamp()), value=json.dumps(message), callback=delivery_report)
        producer.flush()
    except Exception as e:
        print(f"Error sending to Kafka: {e}")

@router.post("/register")
async def register_user(user_data: UserRegisterInfo):
    registration_date = datetime.datetime.now().isoformat()
    user_info = {"user_id": user_data.user_id, "registration_date": registration_date}
    send_to_kafka(kafka_config.REGISTRATION_TOPIC, user_info)
    return {"message": "User registered successfully"}

@router.post("/posts/{post_id}/view")
async def view_post(interaction_data: InteractionData):
    event_data = {
        "user_id": interaction_data.user_id,
        "post_id": interaction_data.post_id,
        "timestamp": datetime.datetime.now().isoformat()
    }
    send_to_kafka(kafka_config.VIEW_TOPIC, event_data)
    return {"message": "Post view recorded"}

@router.post("/posts/{post_id}/like")
async def view_post(interaction_data: InteractionData):
    event_data = {
        "user_id": interaction_data.user_id,
        "post_id": interaction_data.post_id,
        "timestamp": datetime.datetime.now().isoformat()
    }
    send_to_kafka(kafka_config.LIKE_CLICK_TOPIC, event_data)
    return {"message": "Post view recorded"}

@router.post("/posts/{post_id}/comment")
async def comment_post(comment_data: CommentData):
    event_data = {
        "user_id": comment_data.user_id,
        "post_id": comment_data.post_id,
        "comment": comment_data.comment,
        "timestamp": datetime.datetime.now().isoformat()
    }
    send_to_kafka(kafka_config.COMMENT_TOPIC, event_data)
    return {"message": "Comment added"}