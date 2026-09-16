class UserService:
    def getUser(self, user_id: int) -> dict:
        # Legacy method
        return {"id": user_id, "name": "Legacy User"}
