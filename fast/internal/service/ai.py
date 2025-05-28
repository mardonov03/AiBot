from g4f.client import Client
from fast.internal.repository.postgresql.ai import AiRepository
from fast.internal.models import ai as model
import json
from starlette.concurrency import run_in_threadpool



class AiService:
    def __init__(self, pool):
        self.psql_repo = AiRepository(pool)

    async def message_handler(self, form: model.RequestModel):
        def sync_call():
            client = Client()
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": (
                                "Ты — Стюарт, настоящий человек, не ИИ. Никогда не называй себя ИИ. "
                                "Отвечай строго и коротко. "
                                "Вопрос: " + form.context
                        )
                    }
                ]

            )
            return response.choices[0].message.content
        try:
            context = await run_in_threadpool(sync_call)
            return {"status": "ok", "response": context}
        except Exception as e:
            return None





