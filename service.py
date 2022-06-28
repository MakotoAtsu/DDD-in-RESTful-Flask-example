from typing import Optional
from domain.model import Todo_Task
from infrastructure import TaskRepository, FakeMongo

repo = TaskRepository()


def create_new_task(name: str):
    task = repo.create_new_task(Todo_Task(name))
    return {
        'id': task.id,
        'name': task.name,
        'status': 1 if task.status else 0
    }


def update_task_status(task_id: int, name: Optional[str], status: Optional[bool]):
    task = repo.get_task(task_id)
    if not task:
        raise KeyError(f'Specific Task Id:{task_id} dose not exist.')

    if (name):
        task.change_name(name)
    if (status):
        task.change_task_status(status)

    task = repo.update_task(task)
    return {
        'id': task.id,
        'name': task.name,
        'status': 1 if task.status else 0
    }


def remove_task(id: int):
    repo.remove_task(id)


def get_all_tasks() -> list[dict]:
    all_tasks = repo.list_all_tasks()
    return [{
        'id': task.id,
        'name': task.name,
        'status': 1 if task.status else 0
    } for task in all_tasks]
