from g4f.client import Client
from fast.internal.repository.postgresql.ai import AiRepository

class AiService:
    def __init__(self, pool):
        self.psql_repo = AiRepository(pool)
