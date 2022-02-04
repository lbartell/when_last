"""
When Did I Last?
"""
from typing import List
import logging

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.constants import BLUE

from when_last.models.task import Task


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
all_tasks: List[Task] = []


class WhenLast(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.main_box = None
        self.new_task_box = None
        self.task_name_input = None
        self.tasks_box = None

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.create_main_box()
        self.main_window.show()

    def create_main_box(self) -> toga.Box:
        self.main_box = toga.Box(
            style=Pack(direction=COLUMN, padding=5)
        )
        self.main_box.add(self._create_new_task_box())
        self.main_box.add(self._create_tasks_box())
        return self.main_box

    def _create_new_task_box(self) -> toga.Box:
        self.new_task_box = toga.Box(
            style=Pack(direction=ROW, padding=5)
        )

        name_label = toga.Label(
            'Task Name: ',
            style=Pack(padding=(0, 5))
        )
        self.task_name_input = toga.TextInput(style=Pack(flex=1))
        button = toga.Button(
            'Create',
            on_press=self.create_task,
            style=Pack(padding=5)
        )

        self.new_task_box.add(name_label)
        self.new_task_box.add(self.task_name_input)
        self.new_task_box.add(button)

        return self.new_task_box

    def _create_tasks_box(self) -> toga.Box:
        self.tasks_box = toga.Box(
            style=Pack(direction=COLUMN, padding=5)
        )
        return self.tasks_box

    def create_task(self, widget):
        new_task = Task(name=self.task_name_input.value)
        all_tasks.append(new_task)
        logger.info(f"Created new task {new_task.name}")
        self._add_task_to_display(new_task)

    def _add_task_to_display(self, task: Task):
        new_task_box = self._create_task_display_box(task)
        self.tasks_box.insert(0, new_task_box)

    def _create_task_display_box(self, task: Task) -> toga.Box:
        task_label = toga.Label(
            f'Task:\n'
            f' - name: {task.name}\n'
            f' - created: {task.created}',
            style=Pack(padding=(0, 5))
        )
        task_box = toga.Box(style=Pack(direction=ROW, padding=5, background_color=BLUE))
        task_box.add(task_label)
        return task_box


def main():
    return WhenLast()
