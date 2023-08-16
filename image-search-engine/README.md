# Image Search Engine on Shopee

## Environments
### Develop
Development environment that uses PostgreSQL in local and uses the server flask in debug mode.
1. **Create environment and install packages**
    ```shell
    conda create -n image-search python=3.9
    ```
    ```shell
    conda activate image-search
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
    
    Create Database shopee
    ```shell
    CREATE DATABASE db_shopee;
    ```

    Add permission User to Database
    ```shell
    GRANT ALL PRIVILEGES ON DATABASE db_shopee TO db_user;
    ```
### Run
```
uvicorn app:app --reload
```


### Faiss 
To store a FAISS index and its associated data (vectors), you have a few options depending on your requirements:
- **In-Memory Storage**: You can keep the FAISS index and vectors in memory as long as your system has enough RAM to accommodate the data. This is the simplest and fastest option, but it might not be feasible for very large datasets.

- **Disk Storage**: If the entire dataset cannot fit into memory, you can save the FAISS index and vectors to disk using the serialization functionality provided by FAISS. This way, you can load the index back into memory when needed.

- **Database Storage**: For larger datasets that don't fit into memory, you can consider using databases to store the vectors and other metadata. Some popular databases for this purpose are SQLite, PostgreSQL, or MongoDB. In this approach, you would use the FAISS index to perform the search, but the actual vectors are stored and managed in the database.

### Problem
- Issue update faiss store with multiple workers or multiple pods.