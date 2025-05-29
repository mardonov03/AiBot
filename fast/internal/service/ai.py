from g4f.client import Client
from fast.internal.repository.postgresql.ai import AiRepository
from fast.internal.models import ai as model
from starlette.concurrency import run_in_threadpool
from datetime import datetime, timedelta
from fast.internal.core.logging import logger
import json

class AiService:
    def __init__(self, pool):
        self.psql_repo = AiRepository(pool)

    async def _get_active_session(self, userid: int) -> int | None:
        try:
            session = await self.psql_repo.get_last_session(userid)
            if session:
                added_time = datetime.fromtimestamp(session['added_time'])
                if datetime.utcnow() - added_time > timedelta(minutes=15):
                    return None
            return session['sessionid']
        except Exception as e:
            logger.error(f'[_get_active_session error: {e}]')

    async def get_chat_messages(self, sessionid: int, userid: int):
        return await self.psql_repo.get_chat_messages(sessionid, userid)

    async def message_handler(self, form: model.RequestModel):
        try:
            sessionid = await self._get_active_session(form.userid)
            if sessionid:
                chat_messages_json = await self.psql_repo.get_chat_messages(sessionid, form.userid)

                request_message_json = chat_messages_json + [{
                    "role": "user",
                    "content": form.context
                }]
            else:
                request_message_json = [{
                    "role": "user",
                    "content": form.context
                }]

            def sync_call():
                now = datetime.utcnow() + timedelta(hours=5)
                now_str = now.strftime("%Y-%m-%d %H:%M")

                client = Client()
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                f"Дата: {now_str}\n"
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
                        *request_message_json
                    ]
                )
                return response.choices[0].message.content

            response_content = await run_in_threadpool(sync_call)
            response_json = json.loads(response_content)
            if not session:
                sessionid = await self.psql_repo.create_new_session(form.userid, response_json["title"])
            await self.psql_repo.save_message(sessionid, form.userid, "user", form.context)
            await self.psql_repo.save_message(sessionid, form.userid, "assistant", response_json['context'])

            return {"status": "ok", "response": response_content}

        except Exception as e:
            logger.error(f"[message_handler error] {e}")
            raise RuntimeError("Ошибка при обработке сообщения") from e