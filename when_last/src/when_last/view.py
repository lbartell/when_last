from typing import Optional, Dict
import logging
import random

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from travertino import colors

from .model import WhenLastModel, Task
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
        self.tasks: Dict[str, TaskDisplay] = {}

    def create(self) -> toga.Box:
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

    def add_task(self, widget: toga.Button) -> None:
        """Create task and add to view"""
        task_name = self.task_name_input.value

        if task_name in self.tasks:
            # Task already exists, skip.
            logger.info(f"Task {task_name} already exists, skipping creation")
            return

        logger.info(f"Adding new task with name {task_name}")

        task = Task(name=task_name)

        self.controller.add_task(task=task)

        task_display = TaskDisplay(task)
        self.tasks[task_name] = task_display
        self.tasks_display.insert(0, task_display.task_box)


def luminance(rgba: colors.rgba):
    """Calculate luminance from RGB values
    https://en.wikipedia.org/wiki/Relative_luminance
    """
    return 0.2126*rgba.r + 0.7152*rgba.g + 0.0722*rgba.b


class TaskDisplay:
    task_color_options = list(colors.NAMED_COLOR.values())
    time_format = "%Y-%m-%d %H:%M:%S"

    def __init__(self, task: Task):
        self.task = task

        self.task_box: Optional[toga.Box] = None
        self.task_name_label: Optional[toga.Label] = None
        self.last_executed_label: Optional[toga.Label] = None
        self.execute_task_button: Optional[toga.Button] = None

        self._create_display_box()

    def _create_display_box(self) -> toga.Box:
        logger.info(f"Creating task display box for task {self.task}")

        bg_color = colors.NAMED_COLOR['white']
        while luminance(bg_color) > 125:
            bg_color = random.choice(self.task_color_options)

        self.task_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding=5,
                background_color=bg_color
            )
        )

        self.task_name_label = toga.Label(
            self.task.name,
            style=Pack(
                padding=(0, 5)
            )
        )

        self.last_executed_label = toga.Label(
            self._last_executed_label_string(),
            style=Pack(
                padding=(0, 5)
            )
        )

        self.execute_task_button = toga.Button(
            'I Did it!',
            on_press=self.execute_task,
            style=Pack(padding=5)
        )

        self.task_box.add(self.task_name_label)
        self.task_box.add(self.last_executed_label)

        self.task_box.insert(0, self.execute_task_button)

        return self.task_box

    def _last_executed_label_string(self) -> str:
        logger.info(f"Creating 'last executed' label string for task with name {self.task.name}")
        label_str = "Last done: "
        if self.task.execution_times:
            # this task has been done at least once before
            label_str += self.task.execution_times[-1].strftime(self.time_format)
        else:
            # This task has never been done before
            label_str += "never"

        return label_str

    def execute_task(self, widget: toga.Button):
        logger.info(f"Executing task with name {self.task.name}")
        self.task.execute()
        self.last_executed_label.text = self._last_executed_label_string()
        self.task_box.refresh()
