from .model import WhenLastModel, Task


class WhenLastController:

    def __init__(self, model: WhenLastModel):
        self.model = model

    def add_task(self, task: Task):
        self.model.add_task(task=task)

    def execute_task(self, name: str):
        self.model.execute_task(name=name)
