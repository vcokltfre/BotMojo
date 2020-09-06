import json
from pathlib import Path
from discord.ext import commands


class PermissionManager:
    def __init__(self):
        pass

    def get_level(self, uid: int, idtype: str = "role"):
        if idtype == "role":
            return 1000
        elif idtype == "user":
            return 1000

    def resolve_level(self, ctx_or_message):
        user = self.get_level(ctx_or_message.author.id, idtype="user")
        if user: return user

        role_levels = []
        for role in ctx_or_message.author.roles:
            role_levels.append(self.get_level(role.id, idtype="role"))
        return max(role_levels)


class LevelManager:
    def __init__(self):
        with Path("./config/permissions.json").open() as f:
            self.levels = json.load(f)

    def get(self, name: str):
        if name in self.levels:
            return self.levels[name]
        return 10000