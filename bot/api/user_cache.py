class UserCache:
    def __init__(self, size):
        self.users = {}
        self.size = size

    def exists(self, user_id: str):
        return user_id in self.users

    def add(self, user_id: str, data: dict):
        self.users[user_id] = data
        self.ensure_size()

    def get(self, user_id: str):
        if self.exists(user_id):
            return self.users[user_id]
        return None

    def pop(self, user_id: str) -> dict:
        if self.exists(user_id):
            return self.users.pop(user_id)
        return {}

    def update(self, user_id: str, data: dict):
        if self.exists(user_id):
            for key in data:
                self.users[user_id][key] = data[key]
        self.add(user_id, data)

    def ensure_size(self):
        if len(self.users) > self.size:
            self.users.pop(list(self.users.keys())[0])
