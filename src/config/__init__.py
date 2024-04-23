import importlib
import logging
import os
from enum import Enum

_logger = logging.getLogger(__name__)


class Environments(Enum):
    LOCAL = "local"
    PRODUCTION = "production"


ENV = Environments(os.environ.get("ENV", Environments.LOCAL.value))

# Default configs
EXECUTE_API_URL = "https://code-craft-grso.onrender.com/execute"
LANG_API_URL = "https://code-craft-grso.onrender.com/languages"

# pull in the settings from the correct environment
try:
    mod = importlib.import_module(f"{__name__}.{ENV.value}_config")
    for key in dir(mod):
        if key.isupper():
            globals()[key] = mod.__dict__[key]
except ImportError:
    _logger.info(f"Settings file for {ENV.value} environment not found!")

# clean up the exports so that they don't appear in exports
del os
del logging
del importlib
