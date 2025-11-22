Deployment guide — Gunicorn, Docker, DB migrations, SSL
=====================================================

This file contains example steps and configuration to deploy `grievance_portal` in production.

1) Build & run with Docker Compose (recommended)

- Copy the example env file and edit values:

  cp .env.production.example .env.production

- On the server, ensure `docker` and `docker-compose` are installed. Place the project at `/srv/grievance_portal` (or update systemd service path).

- Build and start the stack (this builds the image using `Dockerfile.prod`):

  docker compose -f docker-compose.yml --env-file .env.production up -d --build

- If you want the web container to run migrations automatically, set `RUN_MIGRATIONS=yes` in `.env.production`.

2) Running Alembic migrations manually (on server)

- Enter the web container and run migrations (recommended if you prefer manual control):

  docker compose -f docker-compose.yml --env-file .env.production run --rm web alembic upgrade head

3) Gunicorn command (if you don't use Docker)

- Example (bind port 80):

  gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:80 --workers 3

4) Background workers (Celery)

- The compose file includes a `worker` service that runs Celery. Configure Celery in `app/core/celery_app.py` to use `REDIS_URL`.

5) Database

- Use Postgres or MySQL in production. The compose file uses Postgres. For real production, use a managed DB (RDS, Cloud SQL) and set `DATABASE_URL` accordingly.

6) Domain & SSL (Let's Encrypt)

- Recommended setup: Put an nginx or Traefik reverse proxy in front of the app and obtain TLS certs with Certbot or Traefik's built-in ACME.

- Quick Certbot + nginx example (Debian/Ubuntu):

  apt install nginx certbot python3-certbot-nginx
  # configure nginx to proxy to localhost:80 (or container host port)
  certbot --nginx -d yourdomain.com -d www.yourdomain.com

7) Systemd service example

- See `deploy/systemd/gunicorn-docker-compose.service` — update `WorkingDirectory` to the path where you placed the repo on the server (e.g., `/srv/grievance_portal`).

8) Security / production notes

- Use a strong `SECRET_KEY` and never commit secrets to the repo.
- Run containers as non-root and drop unnecessary capabilities.
- Use a managed DB and backups.
- For email sending, use a reliable SMTP provider and enable TLS.
