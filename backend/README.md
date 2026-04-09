# TicTacToe Backend

This is the backend for tictactoe.com, built with FastAPI and Python.

## Quick Start

We use **uv** for fast dependency management and execution.

### 1. Setup Environment
```bash
# Create virtual environment
uv venv

# Install dependencies
uv pip install -r requirements.txt
```

### 2. Running the Server
```bash
# Start FastAPI server in development mode
uv run uvicorn app.main:app --reload
```

### 3. Running Tests
```bash
# Run the test suite
PYTHONPATH=. uv run pytest
```

### 4. Running Simulation Scripts
```bash
# Run CPU strategy comparison
PYTHONPATH=. uv run python scripts/cpu_comparison.py
```

## Project Structure
- `app/`: Core application logic.
  - `api/`: FastAPI routers (V1, WebSockets).
  - `core/`: Constants, types, and custom exceptions.
  - `schemas/`: Pydantic models for API and WebSockets.
  - `services/`: Business logic, game engine, AI strategies, and ranking.
- `scripts/`: Utility scripts and simulations.
- `tests/`: Project test suite mirroring `app/` structure.
