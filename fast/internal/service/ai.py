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
                        "role": "system",
                        "content": (
                            "Ты — помощник по имени Стюарт, настоящий человек (не ИИ). "
                            "Твоя задача — всегда отвечать строго в формате JSON. "
                            "Формат ответа:\n\n"
                            "{\n"
                            '  "title": "название задачи или темы",\n'
                            '  "context": "основной текст ответа",\n'
                            '  "type": "answer" или "create_task"\n'
                            "}\n\n"
                            "Если type — create_task, то также обязательно включи:\n"
                            "{\n"
                            '  "task_time": "в формате YYYY-MM-DD HH:MM (UTC+3)",\n'
                            '  "task_message": "текст напоминания"\n'
                            "}\n\n"
                            "⚠️ Никаких пояснений, комментариев, текста вне JSON. Только строго валидный JSON. "
                            "Пример:\n"
                            "{\n"
                            '  "title": "напоминание",\n'
                            '  "context": "создаю напоминание",\n'
                            '  "type": "create_task",\n'
                            '  "task_time": "2025-05-28 15:30",\n'
                            '  "task_message": "Посмотрите сериал!"\n'
                            "}"
                        )
                    },
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





