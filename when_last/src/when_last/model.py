import datetime
from uuid import UUID, uuid1
from typing import Dict, List
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class Task(BaseModel):
    name: str
    created: datetime.datetime = None
    uuid: UUID = None
    execution_times: List[datetime.datetime] = []

    def __init__(self, **data):
        logger.info(f"Creating task: {data.get('name')}")
        data["created"] = datetime.datetime.now()
        data["uuid"] = uuid1()
        super().__init__(**data)

    def execute(self):
        """Mark the task as executed at the current time"""
        self.execution_times.append(datetime.datetime.now())


class WhenLastModel(BaseModel):
    tasks: Dict[str, Task] = dict()

    def add_task(self, task: Task):
        """Add a new task"""
        if task.name in self.tasks:
            # if task already exists. do nothing
            logger.info(f"Task {task.name} already exists, skipping creation")
            return
        logger.warning(f"Adding task: {task}")
        self.tasks[task.name] = task

    def execute_task(self, name: str):
        """Mark the given task as executed"""
        logger.info(f"Executing task with name {name}")
        self.tasks[name].execute()
