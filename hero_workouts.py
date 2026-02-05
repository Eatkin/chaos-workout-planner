from hero_workout.runner import Runner

def main() -> None:
    runner = Runner(intensity="medium", location="outdoor", num_exercises=10)
    runner.show_planned()
    runner.run_session()

if __name__ == "__main__":
    main()