from domain.model import Todo_Task


def create_new_task(name: str) -> Todo_Task:
    raise NotImplementedError()


def update_task_name(name: str) -> Todo_Task:
    raise NotImplementedError()


def update_task_status(is_complete: bool) -> Todo_Task:
    raise NotImplementedError()


def remove_task(id: int):
    raise NotImplementedError()


def get_all_task():
    raise NotImplementedError()
