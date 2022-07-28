from pathlib import Path

from . import ConfigsManager

Config = ConfigsManager(Path() / "data" / "configs" / "plugins2config.yaml")
