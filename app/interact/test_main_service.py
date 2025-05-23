import unittest
from unittest.mock import patch, MagicMock
import grpc
import main_service
import proto.main_service_pb2 as pb2
import proto.main_service_pb2_grpc as pb2_grpc
from app.interact.config import kafka_config

class TestCoreService(unittest.TestCase):

    @patch('main_service.KafkaProducer')
    def test_ViewPost_success(self, MockKafkaProducer):
        mock_producer = MagicMock()
        MockKafkaProducer.return_value = mock_producer

        service = main_service.MainService()

        user_id = 123
        post_id = 456

        request = pb2.PostEventRequest(user_id=user_id, post_id=post_id)

        response = service.ViewPost(request, None)

        self.assertEqual(response.success, True)

        mock_producer.send.assert_called_once_with(kafka_config.VIEW_TOPIC, {
            "user_id": user_id,
            "post_id": post_id,
            "timestamp": unittest.mock.ANY
        })
        mock_producer.flush.assert_called_once()

    @patch('main_service.KafkaProducer')
    def test_LikePost_failure(self, MockKafkaProducer):
        mock_producer = MagicMock()
        mock_producer.send.side_effect = Exception("Kafka error")
        MockKafkaProducer.return_value = mock_producer

        user_id = 123
        post_id = 456

        service = main_service.MainService()
        request = pb2.PostEventRequest(user_id=user_id, post_id=post_id)

        response = service.LikePost(request, None)

        self.assertEqual(response.success, False)
        self.assertIn("Kafka error", response.message)
        mock_producer.flush.assert_called_once()

    # def test_GetComments(self):
    #     # Create an instance of the service
    #     service = main_service.SocialMediaService()
    #
    #     # Create a mock request
    #     request = pb2.GetCommentsRequest(post_id="test_post", page=1, page_size=10)
    #
    #     # Call the GetComments method
    #     response = service.GetComments(request, None)
    #
    #     # Assert the results
    #     self.assertIsNotNone(response)
    #     self.assertIsInstance(response, pb2.GetCommentsResponse)
    #     self.assertTrue(len(response.comments) <= 10)  # Ensure page_size is respected
    #     self.assertTrue(response.total_comments >= len(response.comments))

if __name__ == '__main__':
    unittest.main()