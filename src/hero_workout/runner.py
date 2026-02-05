import time
import pyttsx3

from hero_workout.exercise import Exercise
from hero_workout.exercise import load_exercises
from hero_workout.music import MusicHandler
from hero_workout.planner import Planner
from hero_workout.logging_config import get_logger

class Runner:
    def __init__(self, intensity: str = "medium", location: str = "any", num_exercises: int = 10, headless: bool = False) -> None:
        self.logger = get_logger(self.__class__.__name__)
        self.intensity = intensity
        self.location = location
        self.num_exercises = num_exercises
        self.headless = headless # No keyboard
        self.exercises = load_exercises()  # Load all exercises
        self.planner = Planner(self.exercises, intensity=self.intensity, location=self.location)
        self.planned_exercises = self.planner.plan(self.num_exercises)

        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)

        self.music = MusicHandler()

    def _keywait(self, location: str, headless: bool, prep_time: int = 3) -> None:
        if not headless and location.lower() == "indoor":
            input("Press Enter when ready...")
        else:
            self.speak(f"Prep for {prep_time} seconds!")
            time.sleep(prep_time)

    def speak(self, text: str) -> None:
        """TTS and logging."""
        text = text.replace("_", " ").title()
        self.logger.debug(f"Speech: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def prep(self, exercise: Exercise, prep_time: int = 3) -> None:
        """Prep phase before exercise."""
        self.speak(f"Next exercise: {exercise.name}")
        if exercise.assigned_variant:
            self.speak(f"Variant: {exercise.assigned_variant}")
        if exercise.assigned_duration:
            self.speak(f"Duration: {exercise.assigned_duration} seconds")
        if exercise.props:
            self.speak(f"Props needed: {', '.join(exercise.props)}")

        self._keywait(exercise.location, headless=self.headless, prep_time=prep_time)

    def countdown(self, seconds: int = 3) -> None:
        """Countdown before GO."""
        for i in range(seconds, 0, -1):
            self.speak(str(i))
            # 1 second is too slow
            time.sleep(0.5)
        self.speak("GO!")

    def go(self, exercise: Exercise) -> None:
        """Go phase: exercise duration timer."""
        duration = exercise.assigned_duration or 30
        self.speak(f"Start {exercise.name} now!")
        self.music.louden()
        start_time = time.time()
        halfway_called = False

        while time.time() - start_time < duration:
            try:
                elapsed = time.time() - start_time
                if not halfway_called and elapsed >= duration / 2:
                    self.music.quieten()
                    self.speak("Halfway there!")
                    self.music.louden()
                    halfway_called = True
                time.sleep(0.5)
            except KeyboardInterrupt:
                self.speak("Exercise skipped!")
                break

        self.music.quieten()
        self.speak(f"Completed {exercise.name}!")

    def prepare_props(self) -> None:
        """Give you a chance to prepare props for your session."""
        self.speak("Prepare your props!")

        props_by_location = self.planner.get_props_by_location(self.planned_exercises)

        for loc, props in props_by_location.items():
            self.speak(f"{loc.capitalize()} props:")
            for prop in props:
                self.speak(prop)

            time.sleep(0.5)


    def run_session(self) -> None:
        """Iterate through planned exercises."""
        self.music.play()
        self.music.quieten()
        self.prepare_props()
        # ALWAYS keywait after prepare props cause gotta get shit ready and might take a while
        self._keywait("indoor", headless=False)
        for i, ex in enumerate(self.planned_exercises):
            self.music.next_track()
            self.music.quieten()
            self.prep(ex)
            # First go we countdown from a higher number so if outdoors we can get extra time to go out!!
            if i == 0:
                self.countdown(5)
            else:
                self.countdown()
            self.go(ex)
            if i < len(self.planned_exercises) - 1:
                self.speak("Next exercise coming up!")
        self.music.quieten()
        self.speak("Routine completed!")

    def show_planned(self) -> None:
        """Print planned exercises for debug/inspection."""
        for idx, ex in enumerate(self.planned_exercises, start=1):
            self.logger.info(f"{idx}. {ex.name} | Variant: {getattr(ex, 'assigned_variant', None)} "
                  f"| Reps: {getattr(ex, 'assigned_reps', None)} "
                  f"| Duration: {getattr(ex, 'assigned_duration', None)} "
                  f"| Location: {ex.location}")

        props_by_location = self.planner.get_props_by_location(self.planned_exercises)

        idx = 1
        for props in props_by_location.values():
            for prop in props:
                self.logger.info(f"{idx}. {prop}")
                idx += 1