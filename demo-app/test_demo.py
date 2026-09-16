from payment_processor import PaymentProcessor
from user_service import UserService

def test_payment_processor():
    processor = PaymentProcessor()
    assert processor.process_payment(1, 100.0) == True

def test_user_service():
    service = UserService()
    assert service.getUser(1)["name"] == "Legacy User"
