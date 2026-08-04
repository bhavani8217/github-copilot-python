# Sudoku Game

A modern Flask-based Sudoku game enhanced with GitHub Copilot.

## Features

- Difficulty levels (Easy, Medium, Hard)
- Unique Sudoku puzzle generation
- Hint system
- Check Solution
- Real-time validation
- Locked clue cells
- Timer
- Top 10 leaderboard (stored in browser localStorage)
- Dark/Light mode
- Responsive layout

## Installation

```bash
pip install -r requirements.txt
```

## Run the application

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000/
```

## Run tests

```bash
python -m pytest -q
```
## Responsible and Effective Copilot Use

Throughout the project, I reviewed Copilot-generated suggestions before deciding whether to accept them.

As one example, I asked Copilot to generate a Reset Game feature. After reviewing the proposed implementation, I decided not to keep the changes because the feature was outside the scope of the project requirements. I rejected the suggestion using the Undo option instead of accepting unnecessary code.

Evidence of this evaluation is included in the Screenshots folder:
- copilot_review_before_rejection.png
- copilot_rejected_suggestion.png