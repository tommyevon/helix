# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Helix is an investment platform written in Python.

## Commands

```bash
# Run the application
python -m src.main

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Lint and format (via Trunk)
trunk check          # run all linters
trunk fmt            # run all formatters
trunk check --fix    # auto-fix lint issues

# Individual linters
black src/           # format
isort src/           # sort imports
ruff check src/      # fast linting
pylint src/          # static analysis
```

## Architecture

The project is in early stages. Entry point is `src/main.py`. The `src/` package is defined in `src/__init__.py`.

## Linting

Trunk is configured with four linters: **black** (formatting), **isort** (import sorting), **ruff** (fast linting), and **pylint** (static analysis). Pre-commit hooks run `trunk fmt` and pre-push hooks run `trunk check` automatically.
