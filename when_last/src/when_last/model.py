import datetime
import dataclasses
from uuid import UUID, uuid1
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Task:
    name: str
    created: datetime.datetime = None
    uuid: UUID = None
    execution_times: List[datetime.datetime] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        logger.info(f"Creating task: {self.name}")
        self.created = datetime.datetime.now()
        self.uuid = uuid1()

    def execute(self):
        """Mark the task as executed at the current time"""
        self.execution_times.append(datetime.datetime.now())


@dataclasses.dataclass
class WhenLastModel:
    tasks: Dict[str, Task] = dataclasses.field(default_factory=dict)

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
