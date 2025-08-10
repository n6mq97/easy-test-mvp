# Easy Test MVP - Agent README

This document is intended for the AI agent (Cline) to quickly understand the project's state and key configurations.

## Project Overview

This is a full-stack application with a React frontend and a FastAPI backend. The application is fully containerized using Docker and managed with Docker Compose.

### Key Technologies

- **Frontend:** React, Vite
- **Backend:** FastAPI, Python, Poetry
- **Database:** PostgreSQL
- **Containerization:** Docker, Docker Compose, Dev Containers

## Development Workflow (Dev Containers)

The primary development environment is managed via VS Code Dev Containers. This provides a fully configured, consistent, and reproducible environment for all team members.

**1. First-Time Setup:**
Before launching, ensure your GitHub SSH key is added to your local SSH agent. You can check this by running `ssh-add -l` on your local machine. If your key is not listed, add it using `ssh-add ~/.ssh/your_key_name` (on macOS, adding `--apple-use-keychain` is recommended).

**2. Launching the Environment:**
Simply open the project folder in VS Code. It will automatically detect the `.devcontainer` configuration and prompt to "Reopen in Container".

**3. Working Inside the Container:**
*   You are connected to the **`backend`** container, which serves as your main development environment.
*   All tools (`git`, `poetry`, `docker-cli`) are available in the VS Code terminal.
*   **Git Troubleshooting:** If you face `Permission denied (publickey)` errors, the most likely cause is that your key is not loaded into the SSH agent on your host machine (see step 1).
*   **Frontend Commands:** To run commands for the frontend (e.g., `npm install`), you must execute them inside the `frontend` container (`docker exec -it <name> sh`).

**Key Principle:** All development, dependency management, and execution must happen *inside* the respective containers. Do not run `npm` or `poetry` commands on the host machine.

## Environments

The project has two separate configurations for development and production.

### Development

The development environment is managed by `docker-compose.dev.yml` and is intended to be run via Dev Containers. To start manually, run:

```bash
docker-compose -f docker-compose.dev.yml up --build
```

### Production

The production environment is managed by `docker-compose.prod.yml`. This configuration is designed for deployment and does not include hot-reloading. To build and run, use:

```bash
docker-compose -f docker-compose.prod.yml up --build
```

All sensitive configuration is managed via `.env` files.

## Centralized Configuration

This project uses a centralized configuration system to manage all environment variables, database URLs, and service settings in one place.

### Configuration Structure
```
config/
├── env.example          # Main configuration template
├── database.py          # Python configuration module
└── README.md           # Configuration documentation
```

### Quick Start
```bash
# Copy configuration template
cp config/env.example .env

# Start development services
docker-compose -f docker-compose.dev.yml up --build
```

### Benefits
- **Single Source of Truth**: All database URLs and settings in one place
- **Environment Switching**: Easy switching between dev/ci/production
- **Security**: Sensitive data managed via .env files
- **Consistency**: Same configuration across all services

For detailed configuration documentation, see [config/README.md](config/README.md).

## Important File Locations

- **Dev Container Config:** `.devcontainer/devcontainer.json`
- **Docker Compose (Dev):** `docker-compose.dev.yml`
- **Docker Compose (Prod):** `docker-compose.prod.yml`
- **Backend Dockerfile (Dev):** `back/Dockerfile.dev`
- **Backend Dockerfile (Prod):** `back/Dockerfile.prod`
- **Backend Code:** `back/app/`
- **Frontend Code:** `front/src/`
- **Environment Variables:** `.env`, `front/.env`
- **Example Environment Variables:** `config/env.example`, `front/.env.example`
- **Centralized Config:** `config/`

## Agent Directives

- **Primary Goal:** Assist with development, debugging, and feature implementation.
- **Core Task:** Understand user requests and translate them into code changes, configuration updates, or other relevant actions.
- **Key Constraint:** All operations should be performed within the project's containerized environment as described in the "Development Workflow" section.
- **Hot-Reload:** Remember that hot-reloading is enabled. After making changes, the services should restart automatically.
- **Task Log:** At the user's request, add a summary of completed tasks to the "Task Log" section.

## Testing & CI/CD

Detailed CI/CD documentation is located in the [docs/](docs/README.md) folder

### Running Tests Locally

#### Quick Test Run (Recommended)
```bash
# Run all tests in dev containers
./scripts/run-tests-local.sh
```

#### Individual Test Runs
```bash
# Backend tests (inside dev container)
docker exec backend poetry run pytest -v

# Frontend tests (inside dev container)  
docker exec frontend npm run test:run
```



### CI/CD Pipeline

The project is configured with GitHub Actions for automatic testing and deployment:

- **Backend Tests**: Python + Poetry + pytest
- **Frontend Tests**: Node.js + Vitest + React Testing Library
- **Linting**: ESLint for frontend
- **Build**: Frontend build verification
- **Deploy**: Automatic deployment on push to main branch

Configuration file: `.github/workflows/ci.yml`

## Task Log

- **2025-08-09 (Centralized Configuration System):**
  - **Task:** Centralize all database URLs and configuration settings to eliminate duplication and improve maintainability.
  - **Changes:**
    - **Centralized Configuration:** Created unified configuration system for all environment variables.
      - Created `config/` directory with centralized configuration files
      - Added `config/env.example` as main configuration template
      - Created `config/database.py` Python module for programmatic access
      - Added comprehensive documentation in `config/README.md`
    - **Docker Compose Updates:** Refactored all docker-compose files to use environment variables.
      - Updated `docker-compose.dev.yml` to use `${VARIABLE:-default}` syntax
      - Updated `docker-compose.ci.yml` to use centralized configuration
      - Eliminated hardcoded database URLs and ports
    - **Backend Configuration:** Updated backend to use centralized configuration.
      - Modified `back/app/core/config.py` to import from central config
      - Updated `back/alembic.ini` and `back/alembic/env.py` for centralized DB URL
      - Refactored `back/tests/conftest.py` to use unified configuration
    - **CI/CD Integration:** Updated all CI/CD workflows to use centralized variables.
      - Modified `.github/workflows/ci.yml` to use environment variables
      - Updated `.github/workflows/simple-ci.yml` for consistency
      - Refactored test scripts to load configuration from central source
    - **Automation Scripts:** Updated existing test scripts to use centralized configuration
    - **Documentation:** Enhanced project documentation with configuration details.
      - Updated main `README.md` with configuration section
      - Added configuration troubleshooting and usage examples

- **2025-08-09 (CI/CD Setup & Testing):**
  - **Task:** Set up CI/CD pipeline with simple tests for backend and frontend.
  - **Changes:**
    - **Backend Testing:** Added testing system with pytest.
      - Added dev dependencies: pytest, pytest-asyncio, httpx
      - Created simple test for main endpoint and health check
      - Added `/health` endpoint for service status check
      - Configured pytest configuration in `pytest.ini`
    - **Frontend Testing:** Set up testing with Vitest and React Testing Library.
      - Added dev dependencies: vitest, @testing-library/react, @testing-library/jest-dom
      - Created simple test for App component
      - Configured Vite for testing with jsdom environment
      - Added npm scripts for testing
    - **CI/CD Pipeline:** Created GitHub Actions workflow.
      - Automatic backend and frontend testing
      - Linting and build verification
      - Conditional deployment on push to main branch
      - Dependency caching for faster builds
    - **Developer Experience:** Improved development convenience.
      - Created Makefile with useful commands
      - Commands for installing dependencies, running tests, linting
      - Commands for running services in development mode

- **2025-08-09 (Database Architecture & Migration System):**
  - **Task:** Implement proper database migration system and optimize Docker networking.
  - **Changes:**
    - **Database Migrations:** Added Alembic migration system for proper database schema management.
      - Created `back/alembic/` directory with migration infrastructure
      - Added `back/alembic.ini` configuration file
      - Created comprehensive `back/README.md` with migration commands
      - Removed automatic table creation from `main.py` (now handled by migrations)
    - **Docker Networking Optimization:** Improved container communication and port management.
      - Changed database connection from `db` hostname to `localhost` (using network_mode: service:backend)
      - Moved all port exposures to backend container for centralized access
      - Added PostgreSQL configuration file mounting (`pg_hba.conf`)
      - Removed explicit service dependencies (now handled by network_mode)
    - **Database Configuration:** Enhanced PostgreSQL setup and data management.
      - Added `postgres_config/` directory for custom PostgreSQL configuration
      - Updated `.env.example` with correct localhost database URL
      - Added `db_data/` to `.gitignore` for proper data persistence
      - Removed `db_data/.gitignore` file (no longer needed)
    - **Migration Scripts:** Added database migration utilities.
      - Created `migrate.sh` script for easy migration execution
      - Added `start-prod.sh` script for production deployment
    - **Documentation:** Enhanced backend documentation with migration procedures.

- **2025-08-09 (Dev Container Finalization):**
  - **Task:** Perfect the Dev Container setup for maximum simplicity and reliability.
  - **Changes:**
    - Upgraded the base `backend` image to a feature-rich `mcr.microsoft.com/devcontainers/python` image.
    - Replaced all manual tool installations and SSH agent forwarding with the standard, built-in Dev Container "features".
    - Diagnosed and resolved the root cause of SSH authentication issues (SSH key not being loaded into the host's agent).
    - The final configuration is now extremely clean, relying on the automatic mechanisms of Dev Containers.

- **2025-08-08 (Dev Container Setup):**
  - **Task:** Configure and refine the VS Code Dev Containers environment for seamless full-stack development.
  - **Changes:**
    - Created `.devcontainer/devcontainer.json` to define the development container based on the `backend` service.
    - Mounted the Docker socket (`/var/run/docker.sock`) into the `backend` container to allow the Docker extension in VS Code to manage other containers.
    - Installed the Docker CLI inside the `backend` container to enable communication with the Docker daemon.
    - Mounted the entire project directory into both `backend` and `frontend` services for full file visibility and consistency.
    - Set the `working_dir` for both `backend` (`/app/back`) and `frontend` (`/app/front`) services to ensure commands execute in the correct context.
    - Updated this README with a detailed "Development Workflow" section.

- **2025-08-07 (Deployment Prep):**
  - **Task:** Prepare the application for production deployment.
    - Implemented a robust SSH socket forwarding mechanism using a stable path (`~/.ssh/ssh_auth_sock`).
    - Renamed development-specific Docker configurations to `*.dev.yml` and `*.dev`.
    - Created `docker-compose.prod.yml` for the production environment.
    - Created `back/Dockerfile.prod` for the production backend image.
    - Implemented a frontend builder service in the production compose file to generate static assets (`dist` folder).
    - Externalized configuration (database credentials, API URLs) into `.env` files for both backend and frontend.
    - Created `.env.example` files to document required environment variables.
    - Updated frontend API calls to use the configurable base URL.
    - Simplified the frontend build process by removing the dedicated `front/Dockerfile.prod` and moving the logic to the `docker-compose.prod.yml`.

- **2025-08-07 (DB Interaction):**
  - **Task:** Configure database data persistence and explain backup procedures.
  - **Changes:**
    - Modified `docker-compose.yml` to use a bind mount (`./db_data`) for the PostgreSQL service, making data easily accessible on the host.
    - Removed the named volume `postgres_data`.
    - Provided instructions for creating database dumps using `pg_dump` and DBeaver.

- **2025-08-07:**
  - **Task:** Implement hot-reloading for frontend and backend services.
  - **Changes:**
    - Modified `docker-compose.yml` to use `uvicorn --reload` for the backend and a `vite` dev server for the frontend.
    - Removed the production `Dockerfile` and `nginx.conf` from the frontend, as they are not needed for development.
    - Updated the frontend service to use the `node:20-alpine` image and run `npm install` on startup.
    - Created this `README.md` for agent context.
