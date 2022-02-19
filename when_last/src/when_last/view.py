from typing import Optional
import logging

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.constants import BLUE

from .model import WhenLastModel
from .controller import WhenLastController

logger = logging.getLogger(__name__)


class WhenLastView:

    def __init__(self, model: WhenLastModel, controller: WhenLastController):
        logger.info("Initializing view")
        self.model = model
        self.controller = controller

        self.task_name_input: Optional[toga.TextInput] = None
        self.tasks_display: Optional[toga.Box] = None
        self.main_box = self.create()

    def create(self):
        logger.info("Creating view")
        # Create main box
        main_box = toga.Box(
            style=Pack(direction=COLUMN, padding=5)
        )

        # Add "new task creation" section
        new_task_box = toga.Box(
            style=Pack(direction=ROW, padding=5)
        )
        name_label = toga.Label(
            'Task Name: ',
            style=Pack(padding=(0, 5))
        )
        task_name_input = toga.TextInput(style=Pack(flex=1))
        button = toga.Button(
            'Create',
            on_press=self.add_task,
            style=Pack(padding=5)
        )
        new_task_box.add(name_label)
        new_task_box.add(task_name_input)
        new_task_box.add(button)
        main_box.add(new_task_box)
        self.task_name_input = task_name_input  # store for later access

        # Add display for all tasks
        tasks_display = toga.Box(
            style=Pack(direction=COLUMN, padding=5)
        )
        main_box.add(tasks_display)
        self.tasks_display = tasks_display  # store for later access

        return main_box

    def add_task(self, widget: toga.Button):
        """Create task and add to view"""
        task_name = self.task_name_input.value
        logger.info(f"Adding new task with name {task_name}")
        self.controller.add_task(name=task_name)
        task_box = self._create_task_display_box(name=task_name)
        self.tasks_display.insert(0, task_box)

    def _create_task_display_box(self, name: str):
        logger.info(f"Creating task display box for task with name {name}")
        task_label = toga.Label(name, style=Pack(padding=(0, 5)))
        task_box = toga.Box(style=Pack(direction=ROW, padding=5, background_color=BLUE))
        task_box.add(task_label)
        return task_box
