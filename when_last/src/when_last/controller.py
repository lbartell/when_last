from .model import WhenLastModel


class WhenLastController:

    def __init__(self, model: WhenLastModel):
        self.model = model

    def add_task(self, name: str):
        self.model.add_task(name=name)

    def execute_task(self, name: str):
        self.model.execute_task(name=name)
