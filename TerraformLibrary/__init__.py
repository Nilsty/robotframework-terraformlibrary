from .terraformlibrary import TerraformLibrary
from importlib.metadata import version

try:
    __version__ = version("robotframework-terraformlibrary")
except Exception:
    pass