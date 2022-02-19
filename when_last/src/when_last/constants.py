import pathlib
import platformdirs
from .__version__ import version


USER_DATA_DIR = pathlib.Path(platformdirs.user_data_dir(appname='when_last', version=version))
SAVE_PATH = USER_DATA_DIR / "when_last_data" / "model.json"
