## Development Environment

1. **Create Environment and Install Packages**

   ```shell
   conda create -n backend python=3.9
   ```

   ```shell
   conda activate backend
   ```

   ```shell
   pip install -r requirements.txt
   ```

2. **Create PosgresSQL on Ubuntu 20.04**
   Install PosgresSQL

   ```shell
   sudo apt-get install postgresql-12
   ```

   Go in PosgresSQL

   ```shell
   sudo -u postgres psql
   ```

   Create user and password

   ```shell
   CREATE USER db_user WITH PASSWORD 'db_password';
   ```

   Create Database dev

   ```shell
   CREATE DATABASE db_dev;
   ```

   Add permission User to Database

   ```shell
   GRANT ALL PRIVILEGES ON DATABASE db_dev TO db_user;
   ```

3. **Run the Application**
   ```
   uvicorn app:app --port 5000
   ```
