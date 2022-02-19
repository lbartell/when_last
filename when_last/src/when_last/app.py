"""
When Did I Last?
"""
import logging

import toga

from .model import WhenLastModel
from .controller import WhenLastController
from .view import WhenLastView

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(pathname)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class WhenLastApp(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        logger.info("Starting app")

        self.model = WhenLastModel()
        self.controller = WhenLastController(model=self.model)
        self.view = WhenLastView(
            model=self.model,
            controller=self.controller
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.view.main_box
        self.main_window.show()


def main():
    return WhenLastApp()
