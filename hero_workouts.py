from hero_workout.cli import parse_args
from hero_workout.runner import Runner

def main() -> None:
    runner = Runner(**parse_args())
    runner.show_planned()
    runner.run_session()

if __name__ == "__main__":
    main()