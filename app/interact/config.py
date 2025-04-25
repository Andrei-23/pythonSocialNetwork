import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class KafkaConfig:
    BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
    REGISTRATION_TOPIC = os.getenv('KAFKA_REGISTRATION_TOPIC')
    LIKE_CLICK_TOPIC = os.getenv('KAFKA_LIKE_CLICK_TOPIC')
    VIEW_TOPIC = os.getenv('KAFKA_VIEW_TOPIC')
    COMMENT_TOPIC = os.getenv('KAFKA_COMMENT_TOPIC')

kafka_config = KafkaConfig()