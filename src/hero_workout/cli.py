import argparse
from typing import Any
from typing import Dict

from hero_workout.logging_config import get_logger

def parse_args() -> Dict[str, Any]:
    logger = get_logger("ArgParser")
    parser = argparse.ArgumentParser(
        description="Chaos Exercise Planner - your micro-heroic workout!"
    )
    parser.add_argument(
        "--num_exercises", "-n",
        type=int,
        default=10,
        help="Number of exercises to plan in the session"
    )
    parser.add_argument(
        "--location", "-l",
        type=str,
        choices=["indoor", "outdoor", "any"],
        default="any",
        help="Where you want to train"
    )
    parser.add_argument(
        "--headless", "-H",
        action="store_true",
        help="Run fully headless: no keyboard prompts, automatic prep"
    )
    parser.add_argument(
        "--intensity", "-i",
        type=str,
        choices=["easy", "medium", "heroic"],
        default="medium",
        help="Set the intensity level of the workout"
    )

    args = parser.parse_args()

    kwargs = {
        "num_exercises": args.num_exercises,
        "intensity": args.intensity,
        "location": args.location,
        "headless": args.headless
    }
    
    for k, v in kwargs.items():
        logger.info(f"{k}: {v}")

    return kwargs
