# Search Engine Shopee
[![Development](https://github.com/vectornguyen76/search-engine-shopee/actions/workflows/development_pipeline.yml/badge.svg)](https://github.com/vectornguyen76/search-engine-shopee/actions/workflows/development_pipeline.yml)
[![Staging](https://github.com/vectornguyen76/search-engine-shopee/actions/workflows/staging_pipeline.yml/badge.svg)](https://github.com/vectornguyen76/search-engine-shopee/actions/workflows/staging_pipeline.yml)
[![Production](https://github.com/vectornguyen76/search-engine-shopee/actions/workflows/production_pipeline.yml/badge.svg)](https://github.com/vectornguyen76/search-engine-shopee/actions/workflows/production_pipeline.yml)

### Set up development enviroments
1. **Frontend development enviroment**
    - Run backend, database services
        ```
        docker compose --profile dev.frontend up -d
        ```
    - Run frontend
        ```
        cd frontend
        ```
        ```
        npm run dev
        ```
2. **Backend development enviroment**
    - Run frontend, database services
        ```
        docker compose --profile dev.backend up -d
        ```
3. **Production development enviroment**
    - Run all services: backend, frontend, database,...
        ```
        docker compose --profile prod up -d
        ```