## Development Environment

### 1. Create Environment and Install Packages

First, create a virtual environment and install the required packages:

```shell
conda create -n backend python=3.9
conda activate backend
pip install -r requirements.txt
```

### 2. Set Up PostgreSQL on Ubuntu 20.04

Install PostgreSQL:

```shell
sudo apt-get install postgresql-13
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

### 3. Run the Application

To run the application, use the following command:

```shell
uvicorn app:app --port 5000
```

## Database Migrations with Alembic

To manage database migrations, we use Alembic. Here's how to set it up:

1. Initialize Alembic:

   ```shell
   alembic init alembic
   ```

2. Define and generate your first migration:

   Modify the `alembic.ini` configuration file to specify your database connection URL. Then, create an initial migration:

   ```shell
   alembic revision -m "initial2" --autogenerate
   ```

3. Apply the initial migration to the database:

   Apply the migration to create the initial database schema:

   ```shell
   alembic upgrade head
   ```
