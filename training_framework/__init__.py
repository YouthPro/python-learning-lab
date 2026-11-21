"""Public alias to the Phase 3 src-layout package, matching the existing repo pattern."""

from phase3_deep_learning.section09_deep_learning_engineering.projects.pytorch_training_framework.src import (
    training_framework as _implementation,
)

__path__ = _implementation.__path__
__version__ = _implementation.__version__
