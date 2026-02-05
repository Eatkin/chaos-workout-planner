import os
import logging

LOG_LEVEL = logging.DEBUG

DATA_SRC = os.environ.get("DATA_SOURCES_DIR")
if not DATA_SRC:
    raise ValueError("DATA_SOURCES_DIR environment variable not set!!")

HEROIC_EXERCISES = os.path.join(DATA_SRC, "hero_workout", "heroic_exercises.yaml")
MUSIC_SRC = os.path.join(DATA_SRC, "hero_workout", "music")