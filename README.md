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

The primary development environment is managed via VS Code Dev Containers.

1.  **Starting the Environment:** Open the project folder in VS Code. It will automatically detect the `.devcontainer` configuration and prompt to "Reopen in Container". This will build and start all services defined in `docker-compose.dev.yml`.

2.  **Working Environment:**
    *   You are connected to the **`backend`** container. The integrated terminal in VS Code operates within this container.
    *   The entire project directory is mounted at `/app`. The working directory is set to `/app/back`.
    *   All backend-related commands (e.g., `poetry add`, `poetry run`) should be executed directly in the VS Code terminal.

3.  **Interacting with Other Services:**
    *   **Frontend:** To run commands for the frontend (e.g., `npm install <package>`), you must execute them inside the `frontend` container. Use the Docker extension in VS Code or the command `docker exec -it <frontend_container_name> sh`.
    *   **Database:** The database is accessible on `localhost:5432` from the host machine and via the service name `db` from within the other containers.

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

## Important File Locations

- **Dev Container Config:** `.devcontainer/devcontainer.json`
- **Docker Compose (Dev):** `docker-compose.dev.yml`
- **Docker Compose (Prod):** `docker-compose.prod.yml`
- **Backend Dockerfile (Dev):** `back/Dockerfile.dev`
- **Backend Dockerfile (Prod):** `back/Dockerfile.prod`
- **Backend Code:** `back/app/`
- **Frontend Code:** `front/src/`
- **Environment Variables:** `.env`, `front/.env`
- **Example Environment Variables:** `.env.example`, `front/.env.example`

## Agent Directives

- **Primary Goal:** Assist with development, debugging, and feature implementation.
- **Core Task:** Understand user requests and translate them into code changes, configuration updates, or other relevant actions.
- **Key Constraint:** All operations should be performed within the project's containerized environment as described in the "Development Workflow" section.
- **Hot-Reload:** Remember that hot-reloading is enabled. After making changes, the services should restart automatically.
- **Task Log:** At the user's request, add a summary of completed tasks to the "Task Log" section.

## Task Log

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
  - **Changes:**
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
