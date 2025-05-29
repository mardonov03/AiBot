from fast.internal.tasks.task import celery
import asyncio

@celery.task
def reminder(task_message):
    async def wrapper():
        try:
            pass
        except Exception as e:
            print(f"[delete_user error]: {e}")
    asyncio.run(wrapper())
