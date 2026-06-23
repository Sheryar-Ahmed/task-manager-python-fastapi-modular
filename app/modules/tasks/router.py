from fastapi import APIRouter, Depends
from app.modules.tasks.schemas import CreateTaskRequest, UpdateTaskRequest, TaskResponse
from app.modules.tasks.service import get_tasks, get_task, create_task, update_task, delete_task
from app.modules.auth.models import User
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=list[TaskResponse])
async def list_tasks(current_user: User = Depends(get_current_user)):
    tasks = await get_tasks(current_user)
    return [
        TaskResponse(
            id=str(t.id),
            title=t.title,
            description=t.description,
            priority=t.priority,
            status=t.status,
            user_id=t.user_id
        )
        for t in tasks
    ]

@router.post("/", response_model=TaskResponse, status_code=201)
async def create(body: CreateTaskRequest, current_user: User = Depends(get_current_user)):
    task = await create_task(body, current_user)
    return TaskResponse(
        id=str(task.id),
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        user_id=task.user_id
    )

@router.get("/{task_id}", response_model=TaskResponse)
async def get_one(task_id: str, current_user: User = Depends(get_current_user)):
    task = await get_task(task_id, current_user)
    return TaskResponse(
        id=str(task.id),
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        user_id=task.user_id
    )

@router.patch("/{task_id}", response_model=TaskResponse)
async def update(task_id: str, body: UpdateTaskRequest, current_user: User = Depends(get_current_user)):
    task = await update_task(task_id, body, current_user)
    return TaskResponse(
        id=str(task.id),
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        user_id=task.user_id
    )

@router.delete("/{task_id}", status_code=204)
async def delete(task_id: str, current_user: User = Depends(get_current_user)):
    await delete_task(task_id, current_user)