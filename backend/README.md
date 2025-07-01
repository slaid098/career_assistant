# Career Assistant Backend

This directory contains the backend source code for the Career Assistant application.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running with Docker

The simplest way to get the application running is by using Docker Compose. This will build the backend image, start the backend container, and a PostgreSQL database container.

1.  **Navigate to the `backend` directory:**
    ```bash
    cd backend
    ```

2.  **Build and run the containers:**
    ```bash
    docker-compose up --build
    ```

The `--build` flag ensures that the Docker image for the backend is rebuilt if there are any changes to the `Dockerfile` or the source code.

Once the containers are up and running, the API will be accessible at `http://localhost:8000`. You can view the automatically generated API documentation at `http://localhost:8000/docs`.
