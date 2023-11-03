## Development Environment

1. **Create Environment and Install Packages**

   ```shell
   conda create -n image-search python=3.10
   ```

   ```shell
   conda activate image-search
   ```

   ```shell
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```
   uvicorn app:app
   ```
