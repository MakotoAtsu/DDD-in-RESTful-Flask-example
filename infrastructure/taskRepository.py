from typing import Optional
from domain.model import Todo_Task
from .fakeMongo import FakeMongo

database = FakeMongo()


class TaskRepository():

    def __init__(self, ) -> None:
        self._context = database.get_collection('Todo_Tasks')

    def create_new_task(self, task: Todo_Task) -> Todo_Task:
        return self._context.create(task)

    def get_task(self, id: int) -> Todo_Task | None:
        data: Optional[Todo_Task] = self._context.read(id)
        return data

    def update_task(self, task: Todo_Task) -> Todo_Task:
        return self._context.update(task.id, task)

    def remove_task(self, id: int):
        self._context.delete(id)

    def list_all_tasks(self) -> list[Todo_Task]:
        return self._context.list_all()
