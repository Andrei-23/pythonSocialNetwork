import grpc
from fastapi import HTTPException

from proto import main_service_pb2 as pb2
from proto import main_service_pb2_grpc as pb2_grpc

from concurrent import futures
from kafka import KafkaProducer, KafkaConsumer
import json
from datetime import datetime
import threading

from app.interact.config import kafka_config

producer = KafkaProducer(
    bootstrap_servers=kafka_config.BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
consumer = KafkaConsumer(
    kafka_config.COMMENT_TOPIC,
    bootstrap_servers=kafka_config.BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='comment_consumer_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

class MainService(pb2_grpc.MainServiceServicer):
    def ViewPost(self, request, context):
        try:
            event = {
                "user_id": request.user_id,
                "post_id": request.post_id,
                "timestamp": datetime.now().isoformat()
            }
            producer.send(kafka_config.VIEW_TOPIC, event)
            producer.flush()  # Ensure message is sent immediately (for demo)
            print(f"Sent view event: {event}")
            return pb2.PostEventResponse(success=True, message="View recorded")
        except Exception as e:
            print(f"Error sending view event: {e}")
            return pb2.PostEventResponse(success=False, message=str(e))

    def LikePost(self, request, context):
        try:
            event = {
                "user_id": request.user_id,
                "post_id": request.post_id,
                "timestamp": datetime.now().isoformat()
            }
            producer.send(kafka_config.LIKE_CLICK_TOPIC, event)
            producer.flush()
            print(f"Sent like event: {event}")
            return pb2.PostEventResponse(success=True, message="Like recorded")
        except Exception as e:
            print(f"Error sending like event: {e}")
            return pb2.PostEventResponse(success=False, message=str(e))

    def CommentPost(self, request, context):
        try:
            comment_id = 1  # Generate a unique comment ID
            event = {
                "user_id": request.user_id,
                "post_id": request.post_id,
                "comment": request.comment,
                "comment_id": comment_id,  # Include comment ID in event
                "timestamp": datetime.now().isoformat()
            }
            producer.send(kafka_config.COMMENT_TOPIC, event)
            producer.flush()
            print(f"Sent comment event: {event}")
            return pb2.CommentResponse(success=True, message="Comment recorded")
        except Exception as e:
            print(f"Error sending comment event: {e}")
            return pb2.CommentResponse(success=False, message=str(e))

    # def consume_comments():
    #     consumer = KafkaConsumer(
    #         COMMENT_TOPIC,
    #         bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    #         auto_offset_reset='earliest',
    #         enable_auto_commit=True,
    #         group_id='comment_cache_group',
    #         value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    #     )
    #
    #     print("Comment consumer started...")
    #
    #     for message in consumer:
    #         comment_data = message.value
    #         post_id = comment_data.get('post_id')
    #
    #         with comments_cache_lock:  # Protect the cache
    #             if post_id not in comments_cache:
    #                 comments_cache[post_id] = []
    #             comments_cache[post_id].append(comment_data)
    #             print(f"Cached comment for post {post_id}")
    #         # Optionally, you could limit the number of comments stored per post_id
    #         # to prevent the cache from growing too large.

    def GetComments(self, request, context):

        try:
            post_id = request.post_id

            page = request.page
            page_size = request.page_size
            start_index = (page - 1) * page_size
            end_index = start_index + page_size

            comments = []
            paginated_comments = []
            i = 0
            for message in consumer:
                comment_data = message.value
                print(f"message #{i}: {comment_data}")
                if comment_data.get('post_id') == post_id:
                    if start_index <= i < end_index:
                        paginated_comments.append(comment_data)
                    i += 1
                    if i >= end_index:
                        break


            for comment_data in paginated_comments:
                comments.append(pb2.Comment(
                    comment_id=comment_data.get('comment_id', ''),  # Get data from messages
                    user_id=comment_data.get('user_id', ''),
                    comment=comment_data.get('comment', ''),
                    timestamp=comment_data.get('created_at', '')
                ))
            response = pb2.GetCommentsResponse(
                comments=comments,
                comment_cnt=len(comments)
            )
            return response
        except Exception as e:
            print(f"Error reading comments: {e}")
            return pb2.GetCommentsResponse(comments=[], comment_cnt=0)


    def RegisterUser(self, request, context):
        try:
            event = {
                'user_id': request.user_id,
                'username': request.username,
                'registration_date': request.registration_date,
                'timestamp': datetime.now().isoformat()
            }
            producer.send(kafka_config.REGISTRATION_TOPIC, event)
            producer.flush()
            print(f"Sent registration event: {event}")
            return pb2.RegisterResponse(success=True, user_id=request.user_id, message="Registration event recorded")
        except Exception as e:
            print(f"Error sending registration event: {e}")
            return pb2.RegisterResponse(success=False, user_id=0, message=str(e))

def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_MainServiceServicer_to_server(MainService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    run_server()