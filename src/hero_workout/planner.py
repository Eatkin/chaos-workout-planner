from collections import defaultdict
from random import choice
from random import randint
from random import shuffle
from typing import Dict
from typing import List
from typing import Set

from hero_workout.exercise import Exercise
from hero_workout.logging_config import get_logger

class Planner:
    def __init__(self, exercises: List[Exercise], intensity: str, location: str):
        self.logger = get_logger(self.__class__.__name__)
        self.location = location
        self.exercises = [ex for ex in exercises if self._filter_exercise(ex)]
        if not self.exercises:
            raise RuntimeError("No exercises could be found given the constraints!!")
        self.intensity = intensity

        # Derived properties
        self.exercises_by_category = defaultdict(list)
        for e in self.exercises:
            self.exercises_by_category[e.category].append(e)

        # Shuffle
        for k in self.exercises_by_category.keys():
            shuffle(self.exercises_by_category[k])

        self.categories = list(self.exercises_by_category.keys())

    def get_props_by_location(self, plan: List[Exercise]) -> Dict[str, Set[str]]:
        props_by_location = defaultdict(set)
        for e in plan:
            for prop in e.props:
                props_by_location[e.location].add(prop)

        return dict(props_by_location)

    def _filter_exercise(self, ex: Exercise) -> bool:
        if ex.location == self.location or self.location == "any" or ex.location == "any":
            return True
        return False

    def _sort_plan(self, planned: List[Exercise]) -> List[Exercise]:
        """Sort to make indoor appear before outdoor"""
        # No sorting if exercises aren't mixed
        if self.location != "any":
            return planned
        planned = sorted(planned, key=lambda e: e.location)
        return planned

    def plan(self, num_exercises: int) -> List[Exercise]:
        planned: List[Exercise] = []
        while len(planned) < num_exercises:
            # Circuit breaker if we've picked everything
            self.categories = list(self.exercises_by_category.keys())
            if not self.categories:
                self.logger.debug("Categories exhausted")
                break
            
            category = choice(self.categories)
            candidates: List[Exercise] = [e for e in self.exercises_by_category[category]
              if not planned or e.name != planned[-1].name]

            if not candidates:
                # There will never be anymore candidates if there's one category and zero candidates
                if len(self.exercises_by_category) == 1:
                    self.logger.debug("Nothing to add without repeats")
                    break
                continue

            ex = candidates[0]

            ex_copy = Exercise(**ex.__dict__)  # shallow copy
            if ex_copy.max_reps > 1:
                # Reduce reps by one and shuffle
                ex.max_reps -= 1
                shuffle(self.exercises_by_category[category])
            else:
                self.exercises_by_category[category].remove(ex)

            # Remove category if empty
            if not self.exercises_by_category[category]:
                self.exercises_by_category.pop(category)

            # pick random variant if exists
            if ex_copy.variants:
                ex_copy.assigned_variant = choice(ex_copy.variants)

            # pick reps/duration for intensity
            if ex_copy.duration_sec:
                min_sec, max_sec = ex_copy.duration_sec[self.intensity]
                ex_copy.assigned_duration = randint(min_sec, max_sec)

            # Resolve 'any' to either indoor our outdoor
            if ex_copy.location == "any":
                ex_copy.location = choice(["indoor", "outdoor"])

            planned.append(ex_copy)

            self.logger.debug(f"{ex_copy.name} | Category: {category} | Variant: {getattr(ex_copy, 'assigned_variant', None)} | Duration: {getattr(ex_copy, 'assigned_duration', None)}")

        return self._sort_plan(planned)
