# Project structure

This repository follows a clear separation of concerns with a frontend and a backend, plus tests and Docker configuration.

## Layout

- `backend/`: Flask API (business logic, routes, models, services, utilities)
- `frontend/`: Web UI (React/Vite)
- `tests/`: automated tests (pytest)
- `data/seed/`: minimal seed data for development/testing only
- `docker-compose.*.yaml`: container orchestration (dev/prod)
- `requirements.txt`: pinned Python dependencies
- `requirements-test.txt`: pinned test dependencies
- `.pre-commit-config.yaml`: formatting and linting hooks

## Data management

Runtime data is not versioned. Only minimal seed files are present in `data/seed/`.
