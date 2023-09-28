# Search Engine Shopee
[![Development](https://github.com/vectornguyen76/search-engine-shopee/actions/workflows/development_pipeline.yml/badge.svg)](https://github.com/vectornguyen76/search-engine-shopee/actions/workflows/development_pipeline.yml)
[![Staging](https://github.com/vectornguyen76/search-engine-shopee/actions/workflows/staging_pipeline.yml/badge.svg)](https://github.com/vectornguyen76/search-engine-shopee/actions/workflows/staging_pipeline.yml)
[![Production](https://github.com/vectornguyen76/search-engine-shopee/actions/workflows/production_pipeline.yml/badge.svg)](https://github.com/vectornguyen76/search-engine-shopee/actions/workflows/production_pipeline.yml)

## Text Search Engine
### Full text search
    - Implement by Elasticsearch

### Autocomplete
    - Implement by Elasticsearch

### Semantic Search
    - Implement by Elasticsearch/Qdrant
    - Semantic Search with text to text
    - Semantic Search with text to image

## Set up enviroment develop
### Develop frontend
- Run backend services
    ```
    docker compose --profile dev.frontend up
    ```
- Run frontend
    ```
    cd frontend
    ```
    ```
    npm run dev
    ```
### Develop backend
- Run f services
    ```
    docker compose --profile dev.frontend up
    ```
- Run frontend
    ```
    cd frontend
    ```
    ```
    npm run dev
    ```
- docker compose --profile dev.backend up
### Develop production
- docker compose --profile prod up

### Reference 
- https://www.sbert.net/examples/applications/image-search/README.html

## Image Search Engine
