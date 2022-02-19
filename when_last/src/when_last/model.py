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
    times_executed: List[datetime.datetime] = []

    def __init__(self, **data):
        logger.info(f"Creating task: {data.get('name')}")
        data["created"] = datetime.datetime.now()
        data["uuid"] = uuid1()
        super().__init__(**data)

    def execute(self):
        """Mark the task as executed at the current time"""
        self.times_executed.append(datetime.datetime.now())


class WhenLastModel(BaseModel):
    tasks: Dict[str, Task] = dict()

    def add_task(self, name: str):
        """Add a new task"""
        logger.info(f"Adding task with name {name}")
        if name in self.tasks:
            # if task already exists. do nothing
            logger.info(f"Task {name} already exists, skipping creation")
            return
        logger.warning(f"Adding task with name: {name}")
        self.tasks[name] = Task(name=name)

    def execute_task(self, name: str):
        """Mark the given task as executed"""
        logger.info(f"Executing task with name {name}")
        self.tasks[name].execute()
