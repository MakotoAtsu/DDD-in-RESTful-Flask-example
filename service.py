from typing import Optional
from domain.model import Todo_Task
from infrastructure import TaskRepository, FakeMongo

db = FakeMongo()


def create_new_task(name: str) -> Todo_Task:
    repo = TaskRepository(db)
    task = repo.create_new_task(name)
    return task


def update_task_status(task_id: int, name: Optional[str], status: Optional[bool]) -> Todo_Task:
    repo = TaskRepository(db)
    task = repo.get_task(task_id)
    if not task:
        raise KeyError(f'Specific Task Id:{task_id} dose not exist.')

    if (name):
        task.change_name(name)
    if (status):
        task.change_task_status(status)

    return repo.update_task(task)


def remove_task(id: int):
    repo = TaskRepository(db)
    repo.remove_task(id)


def get_all_task() -> list[Todo_Task]:
    repo = TaskRepository(db)
    all_tasks = repo.list_all_tasks()
    return all_tasks
