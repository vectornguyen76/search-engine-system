# Search Engine Backend

## Index

- [Overview](#overview)
- [Environments](#environments)
  - [Develop](#develop)
  - [Local - Docker](#local---docker)
- [Reference](#reference)

## Overview

- Dockerfile optimized for small size and fast builds with a non-root user
- Easy local development environment with configured PostgreSQL
- SQLAlchemy with slightly configured `alembic`
- Async SQLAlchemy engine
- Migrations set in an easy-to-sort format (`YYYY-MM-DD_slug`)
- Pre-installed JWT authorization
- Short-lived access token
- Long-lived refresh token stored in http-only cookies

## Environments

### Develop

1. **Create Environment and Install Packages**

   First, create a virtual environment and install the required packages:

   ```shell
   conda create -n backend python=3.10
   conda activate backend
   pip install -r requirements.txt
   ```

2. **Set Up PostgreSQL on Ubuntu 20.04**

   Install PostgreSQL:

   ```shell
   sudo apt-get install postgresql-14
   ```

   Access the PostgreSQL command line:

   ```shell
   sudo -u postgres psql
   ```

   Create a user and password for your database:

   ```shell
   CREATE USER db_user WITH PASSWORD 'db_password';
   ```

   Create a database named 'db_dev':

   ```shell
   CREATE DATABASE db_dev;
   ```

   Grant all privileges to the user for the 'db_dev' database:

   ```shell
   GRANT ALL PRIVILEGES ON DATABASE db_dev TO db_user;
   ```

   If you need to reset the database, you can drop it:

   ```shell
   DROP DATABASE IF EXISTS db_dev;
   ```

   Connect to the 'db_dev' database:

   ```shell
   sudo -u postgres psql -d db_dev
   ```

   List Tables:

   To list all the tables in the current schema (usually "public"), you can use the following SQL command within the psql session:

   ```
   \dt
   ```

3. **Migrations**

   1. Initialize Alembic:

      ```shell
      alembic init alembic
      ```

   2. Define and generate your first migration:

      Modify the `alembic.ini` configuration file to specify your database connection URL. Then, create an initial migration:

      ```shell
      alembic revision -m "initial" --autogenerate
      ```

   3. Apply the initial migration to the database:

      Apply the migration to create the initial database schema:

      ```shell
      alembic upgrade head
      ```

   4. Create .env from .env.example
      - Generate Secret key:
      ```
      openssl rand -hex 32
      ```

4. **Run the Application**

   ```shell
   uvicorn app:app --port 5000
   ```

### Local - Docker

1. **Build Docker Image**

   ```shell
   docker compose build
   ```

2. **Run Containers**

   ```shell
   docker compose up -d
   ```

3. **Migrations**

   - Create an automatic migration from changes in `src/database.py`

     ```shell
     docker compose exec backend_service makemigrations *migration_name*
     ```

   - Run migrations

     ```shell
     docker compose exec backend_service migrate
     ```

   - Downgrade migrations

     ```shell
     docker compose exec backend_service downgrade -1  # or -2 or base or hash of the migration
     ```

## Reference

- [fastapi_production_template](https://github.com/zhanymkanov/fastapi_production_template)
- [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [fastapi_sqlalchemy_async_orm](https://github.com/nf1s/fastapi_sqlalchemy_async_orm)
- [Tutorial: FastAPI with SQLAlchemy Async ORM and Alembic](https://ahmed-nafies.medium.com/tutorial-fastapi-with-sqlalchemy-async-orm-and-alembic-2fa68102f82d)
