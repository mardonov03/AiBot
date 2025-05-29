from tasks.task import celery
import asyncio
from tgbot.handlers.message_handler import send_message_handler

@celery.task
def reminder(task_message, userid):
    async def wrapper():
        try:
            await send_message_handler(userid, task_message)
        except Exception as e:
            print(f"[reminder task error]: {e}")
    asyncio.run(wrapper())
