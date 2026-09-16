class UserRepository:
    def findById(self, user_id: int) -> dict:
        # New method
        return {"id": user_id, "name": "New User"}
