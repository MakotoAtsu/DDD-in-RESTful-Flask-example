from typing import Optional
from domain.model import Todo_Task
from infrastructure import TaskRepository

repo = TaskRepository()


def create_new_task(name: str):
    task = repo.create(Todo_Task(name))
    return {
        'id': task.id,
        'name': task.name,
        'status': 1 if task.status else 0
    }


def update_task(task_id: int, name: Optional[str] = None, status: Optional[bool] = None):
    task = repo.read(task_id)
    if not task:
        raise KeyError(f'Specific Task Id:{task_id} dose not exist.')

    if (name):
        task.change_name(name)
    if (status):
        task.change_task_status(status)

    task = repo.update(task)
    return {
        'id': task.id,
        'name': task.name,
        'status': 1 if task.status else 0
    }


def remove_task(id: int):
    repo.delete(id)


def get_all_tasks() -> list[dict]:
    all_tasks = repo.list_all()
    return [{
        'id': task.id,
        'name': task.name,
        'status': 1 if task.status else 0
    } for task in all_tasks]
