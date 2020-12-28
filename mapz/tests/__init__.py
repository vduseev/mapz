"""Turn off flake8 deprecation warnings."""

from logging import getLogger

getLogger("flake8").propagate = False
