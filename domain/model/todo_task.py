
class Todo_Task():
    def __init__(self,  name: str) -> None:
        self.id: int = 0
        self.name: str = name
        self.status: bool = False

    def change_name(self, new_name: str):
        if (not new_name or not len(new_name)):
            raise ValueError("Cannot change to empty")
        self.name = new_name
        return self

    def change_task_status(self, isComplete: bool):
        self.status = bool(isComplete)
        return self
