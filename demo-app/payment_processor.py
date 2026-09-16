from user_service import UserService

class PaymentProcessor:
    def __init__(self):
        self.user_service = UserService()

    def process_payment(self, user_id: int, amount: float):
        user = self.user_service.getUser(user_id)
        print(f"Processing ${amount} for {user['name']}")
        return True
