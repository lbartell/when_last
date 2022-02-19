from __future__ import annotations
import datetime
import pathlib
from uuid import UUID, uuid1
from typing import Dict, List
import logging
import json

from pydantic import BaseModel

from . import constants

logger = logging.getLogger(__name__)


class Task(BaseModel):
    name: str
    created: datetime.datetime = None
    uuid: UUID = None
    execution_times: List[datetime.datetime] = []

    def __init__(self, **data):
        logger.info(f"Creating task: {data.get('name')}")
        data['created'] = datetime.datetime.now()
        data['uuid'] = uuid1()
        super().__init__(**data)

    def execute(self):
        """Mark the task as executed at the current time"""
        self.execution_times.append(datetime.datetime.now())


class WhenLastModel(BaseModel):
    tasks: Dict[str, Task] = dict()
    save_path: pathlib.Path = constants.SAVE_PATH

    def add_task(self, task: Task):
        """Add a new task"""
        if task.name in self.tasks:
            # if task already exists. do nothing
            logger.info(f"Task {task.name} already exists, skipping creation")
            return
        logger.warning(f"Adding task: {task}")
        self.tasks[task.name] = task
        self.save(path=self.save_path)

    def remove_task(self, task: Task):
        task_name = task.name
        logger.info(f"Removing task with name {task_name}")
        if task_name not in self.tasks:
            logger.warning(f"Task {task_name} does not exist in tasks, unable to remove")
            return

        del self.tasks[task_name]
        logger.info(f"Removed task with name {task_name}")

    def execute_task(self, name: str):
        """Mark the given task as executed"""
        logger.info(f"Executing task with name {name}")
        self.tasks[name].execute()
        self.save(path=self.save_path)

    def save(self, path: pathlib.Path):
        """Save to json file"""
        full_path = path.resolve()
        logger.info(f"Saving data to file: {full_path}")
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w') as f:
            json.dump(self.dict(), f, default=str, indent=4)

    @classmethod
    def load(cls, path: pathlib.Path) -> WhenLastModel:
        """Load from saved json file"""
        logger.info(f"Loading data from path {path}")

        # If path doesn't exist, just create a new model
        if not path.exists():
            logger.info(f"Data file {path} does not exist. Creating new model")
            return cls()

        # Load model from file
        with open(path) as f:
            data = json.load(f)
        logger.info(f"Loaded data from path {path}")
        return cls(**data)

