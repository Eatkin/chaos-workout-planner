# Chaos Exercise Planner

Do you find home workout apps dreadfully tedious and boring?

Do you want something that's more...personal? Such as bicep curls followed by solving a Rubik's cube then balancing a broom pole on your nose?

Chaos Exercise Planner is a fun, chaotic, randomised exercise routine generator! Mix and match different categories to insert anything you want into your routines! Optional background music to get you pumped!

## Quick Start

### Prerequisites

- Python 3.10+  
- pip package manager  
- Optional: speakers/headphones for text-to-speech and music  

### 1. Set up configuration / environment

Create a `.env` file with your data sources directory:

```bash
cat <<EOF > .env
export DATA_SOURCES_DIR="/path/to/data_sources"
EOF
```

Load it:

```bash
source .env
```

The folder should contain:

- `hero_workout/heroic_exercises.yaml` - the exercise definitions  
- `hero_workout/music/` - optional folder of music tracks (mp3, wav, ogg supported)  

---

### 2. Install dependencies

Install the project as a package in a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

Or using `requirements.txt` if you prefer:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 3. Run the project

Use the entrypoint:

```bash
python hero_workouts.py
```

Get CLI help:

```bash
python hero_workouts.py -h
```

Example:

```bash
python hero_workouts.py --location indoor --headless --intensity heroic --num_exercises 1000
```

- `headless` - no keyboard intervention after the initial start  
- `indoor` vs `outdoor` - exercises are sorted so indoor exercises come first; no keyboard needed outdoors  

---

### 4. Test the project

NOTE: There are no tests (yet)

```bash
pytest tests/
```

---

## Project Structure

- `src/hero_workout/` - main application code  
  - `planner.py` - exercise planning logic  
  - `runner.py` - executes a planned session with optional TTS and music  
  - `music_handler.py` - music playback and management  
  - `config.py` - paths, environment, logging  
- `tests/` - test suite  
- `README.md` - this file  
- `pyproject.toml` / `requirements.txt` - dependencies  
- `heroic_exercises.example.yaml` - example exercise YAML  

---

## Notes

- `max_reps` is optional in YAML, defaults to 1  
- Indoor/outdoor logic: indoor exercises run first; outdoor exercises require no keyboard  
- `location: any` will randomly assign indoor or outdoor
- Customise `src/hero_workout/config.py` for your own paths, logging level, and music folder  
