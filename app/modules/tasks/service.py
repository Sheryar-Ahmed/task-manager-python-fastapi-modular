from app.modules.tasks.models import Task
from app.modules.tasks.schemas import CreateTaskRequest, UpdateTaskRequest
from app.modules.auth.models import User
from app.core.exceptions import raise_not_found_exception, raise_forbidden_exception

async def get_tasks(user: User) -> list[Task]:
    return await Task.find({"user_id": str(user.id)}).to_list()

async def get_task(task_id: str, user: User) -> Task:
    task = await Task.get(task_id)

    if not task:
        raise_not_found_exception("Task not found")

    if task.user_id != str(user.id):
        raise_forbidden_exception("You don't own this task")

    return task

async def create_task(data: CreateTaskRequest, user: User) -> Task:
    task = Task(
        title=data.title,
        description=data.description,
        priority=data.priority,
        status=data.status,
        user_id=str(user.id)
    )
    await task.insert()
    return task

async def update_task(task_id: str, data: UpdateTaskRequest, user: User) -> Task:
    task = await get_task(task_id, user)
    updates = data.model_dump(exclude_none=True)
    if updates:
        await task.set(updates)
    return task

async def delete_task(task_id: str, user: User) -> None:
    task = await get_task(task_id, user)
    await task.delete()