from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional

import yaml

from hero_workout.config import HEROIC_EXERCISES

@dataclass
class Exercise:
    name: str
    category: str
    location: str
    props: list[str]
    max_reps: int = 1
    assigned_duration: Optional[int] = None
    duration_sec: Optional[Dict[str, List[int]]] = None
    assigned_variant: Optional[str] = None
    variants: Optional[List[str]] = None

def load_exercises() -> List[Exercise]:
    with open(HEROIC_EXERCISES, "r") as f:
        data = yaml.safe_load(f)
    exercises = []
    # Parse
    for category, exercises_list in data['categories'].items():
        for e in exercises_list:
            exercise = Exercise(**e, category=category)
            exercises.append(exercise)

    return exercises
        

    