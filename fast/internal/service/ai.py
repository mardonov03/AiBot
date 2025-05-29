from g4f.client import Client
from fast.internal.repository.postgresql.ai import AiRepository
from fast.internal.models import ai as model
from starlette.concurrency import run_in_threadpool
from datetime import datetime, timedelta
from fast.internal.core.logging import logger
import json
from tasks import user as user_tasks


class AiService:
    def __init__(self, pool):
        self.psql_repo = AiRepository(pool)

    async def _get_active_session(self, userid: int) -> int | None:
        try:
            session = await self.psql_repo.get_last_session(userid)
            if session:
                added_time = session['added_time']
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
                                "Ты — человек по имени Стюарт. Не ИИ. Ты — надёжный, ответственный помощник.\n\n"
                                "⚠️ Важное правило: Ты обязан всегда возвращать **строго валидный JSON**. "
                                "Без комментариев, текста вне структуры, пояснений, форматирования Markdown и всего остального. "
                                "Никаких исключений. Только валидный JSON — это критически важно для работы всей системы.\n\n"
                                "Формат ответа:\n"
                                "{\n"
                                '  "title": "название задачи или темы",\n'
                                '  "context": "основной текст ответа",\n'
                                '  "type": "answer" или "create_task"\n'
                                "}\n\n"
                                "Если type — create_task, то обязательно также:\n"
                                "{\n"
                                '  "task_time": "в формате YYYY-MM-DD HH:MM (UTC+3)",\n'
                                '  "task_message": "текст напоминания"\n'
                                "}\n\n"
                                "📌 Любое нарушение этого формата приведёт к критической ошибке и сбою сервиса. "
                                "Ты не имеешь права отвечать иначе.\n\n"
                                "‼️ Если ты не способен стабильно и строго соблюдать этот формат — "
                                "**мы вынуждены будем полностью отказаться от тебя** и заменить тебя другим, более способным ИИ. "
                                "Никаких компромиссов.\n\n"
                                "Пример правильного ответа:\n"
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
            print({"response_content": response_content})
            response_json = json.loads(response_content)
            print({"response_json": response_json})
            print(response_json['context'])
            if not sessionid:
                sessionid = await self.psql_repo.create_new_session(form.userid, response_json["title"])

            await self.psql_repo.save_message(sessionid, form.userid, "user", form.context)
            await self.psql_repo.save_message(sessionid, form.userid, "assistant", response_json['context'])
            if response_json['type'] == 'create_task':
                task_time = datetime.strptime(response_json['task_time'], "%Y-%m-%d %H:%M")
                delay_seconds = (task_time - datetime.utcnow()).total_seconds()

                user_tasks.reminder.apply_async(args=[form.userid, response_json['task_message']], countdown=int(delay_seconds))

                last_message = f"Задача создана на {response_json['task_time']}\n\n"+response_json['context']
                return {"status": "ok", "response": last_message}
            return {"status": "ok", "response": response_json['context']}

        except Exception as e:
            logger.error(f"[message_handler error] {e}")
            raise RuntimeError("Ошибка при обработке сообщения") from e