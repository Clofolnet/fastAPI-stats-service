# FastAPI - Stat service

# Launching a project with Docker:
1. `git clone https://github.com/Clofolnet/fastAPI-stats-service`
2. `cd fastAPI-stats-service`
3. `Rename the .env.docker file to .env`
4. `docker compose up --build -d`
5. `docker compose exec web alembic upgrade head`
6. Complete

# Running tests with a Docker:
1. `git clone https://github.com/Clofolnet/fastAPI-stats-service`
2. `cd fastAPI-stats-service`
3. `Rename the .env.docker file to .env`
4. `docker compose up --build -d`
5. `docker compose exec web alembic upgrade head`
6. `docker compose exec web python3 -m pytest tests`
7. Complete

Endpoint map with documentation for 0.0.0.0 (port 8004) with Docker:
- Swagger <a href="http://0.0.0.0:8004/docs">http://0.0.0.0:8004/docs

Endpoint map with documentation for 127.0.0.1 (standard host + port) without Docker:
- Swagger <a href="http://127.0.0.1:8000/docs">http://127.0.0.1:8000/docs

