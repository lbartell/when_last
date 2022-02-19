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

        self.tasks: Dict[str, TaskDisplay] = {}

        self.task_name_input: Optional[toga.TextInput] = None
        self.tasks_display: Optional[toga.Box] = None
        self.main_box = self.create()

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
        task_name_input = toga.TextInput(
            style=Pack(width=150)
        )
        button = toga.Button(
            'Create',
            on_press=self.create_task,
            style=Pack(padding=5)
        )
        new_task_box.add(name_label)
        new_task_box.add(task_name_input)
        new_task_box.add(button)
        main_box.add(new_task_box)
        self.task_name_input = task_name_input  # store for later access

        # Add display for all tasks
        tasks_display = toga.Box(
            style=Pack(direction=COLUMN, padding=5, flex=1)
        )
        main_box.add(tasks_display)
        self.tasks_display = tasks_display  # store for later access

        # Add all existing tasks to the display
        for task_name, task in self.model.tasks.items():
            self.display_task(task)

        return main_box

    def create_task(self, widget: toga.Button) -> None:
        """Create task and add to view"""
        task_name = self.task_name_input.value

        if task_name in self.tasks:
            # Task already exists, skip.
            logger.info(f"Task {task_name} already exists, skipping creation")
            return

        logger.info(f"Adding new task with name {task_name}")

        task = Task(name=task_name)
        self.controller.add_task(task=task)
        self.display_task(task=task)

    def display_task(self, task: Task):
        """Create task display box and display it"""
        task_display = TaskDisplay(task=task, view=self)
        self.tasks[task.name] = task_display
        self.tasks_display.insert(0, task_display.task_box)

    def remove_task(self, task: Task):
        """Delete task from data and remove from view"""
        logger.info(f"Removing task {task.name}")
        task_name = task.name

        # Remove from display
        self.tasks_display.remove(self.tasks[task_name].task_box)

        # Remove from tasks
        del self.tasks[task_name]

        # Remove from model
        self.model.remove_task(task)


def luminance(rgba: colors.rgba):
    """Calculate luminance from RGB values
    https://en.wikipedia.org/wiki/Relative_luminance
    """
    return 0.2126*rgba.r + 0.7152*rgba.g + 0.0722*rgba.b


class TaskDisplay:
    task_color_options = list(colors.NAMED_COLOR.values())
    time_format = "%a %b %-d %Y, %-I:%M:%S %p"

    def __init__(self, task: Task, view: WhenLastView):
        self.task = task
        self.view = view
        self.model = view.model

        self.task_box: Optional[toga.Box] = None
        self.task_name_label: Optional[toga.Label] = None
        self.last_executed_label: Optional[toga.Label] = None
        self.execute_task_button: Optional[toga.Button] = None
        self.remove_task_button: Optional[toga.Button] = None

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
                background_color=bg_color,
            )
        )

        self.execute_task_button = toga.Button(
            self.task.name,
            on_press=self.execute_task,
            style=Pack(
                padding=5
            )
        )

        fill_box = toga.Box(
            style=Pack(
                flex=1
            )
        )

        self.last_executed_label = toga.Label(
            self._last_executed_label_string(),
            style=Pack(
                padding=(0, 5)
            )
        )

        self.remove_task_button = toga.Button(
            'X',
            on_press=self.remove_task,
            style=Pack(
                padding=5
            )
        )

        self.task_box.add(self.execute_task_button)
        self.task_box.add(fill_box)
        self.task_box.add(self.last_executed_label)
        self.task_box.add(self.remove_task_button)

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
        self.model.execute_task(name=self.task.name)
        self.last_executed_label.text = self._last_executed_label_string()
        self.task_box.refresh()

    def remove_task(self, widget: toga.Button):
        logger.info(f"Removing task {self.task.name}")
        self.view.remove_task(self.task)
