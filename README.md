# Search Engine System

[![Development](https://github.com/vectornguyen76/search-engine-system/actions/workflows/development_pipeline.yml/badge.svg)](https://github.com/vectornguyen76/search-engine-system/actions/workflows/development_pipeline.yml)
[![Staging](https://github.com/vectornguyen76/search-engine-system/actions/workflows/staging_pipeline.yml/badge.svg)](https://github.com/vectornguyen76/search-engine-system/actions/workflows/staging_pipeline.yml)
[![Production](https://github.com/vectornguyen76/search-engine-system/actions/workflows/production_pipeline.yml/badge.svg)](https://github.com/vectornguyen76/search-engine-system/actions/workflows/production_pipeline.yml)

A scalable search engine system supporting both image and text search capabilities using vector similarity.

<p align="center">
  <img src="./assets/gifs/image-search-demo.gif" alt="Image Search" />
  <br>
  <em>Image Search</em>
</p>

<p align="center">
  <img src="./assets/gifs/text-search-demo.gif" alt="Text Search" />
  <br>
  <em>Text Search</em>
</p>

## System Architecture

<p align="center">
  <img src="./assets/images/architectures.png" alt="Architecture" />
  <br>
  <em>System Architecture</em>
</p>

## Features

- **Image Search Engine**: Search for similar images using deep learning embeddings

  - [Detailed Documentation](./image-search-engine/README.md)
  - Vector similarity search using Qdrant
  - Support for multiple image formats
  - Real-time image processing and embedding generation
  - Based on ResNet/EfficientNet architecture for feature extraction

- **Text Search Engine**: Advanced text search with Elasticsearch
  - [Detailed Documentation](./text-search-engine/README.md)
  - Dual search capabilities:
    - Autocomplete (Search-as-you-type) using Edge NGram Tokenizer
    - Full-text search with fuzzy matching
  - Custom scoring based on business metrics
  - Multi-field search across item and shop names
  - Support for Vietnamese language

## Technical Details

### Image Search Pipeline

- **Preprocessing**:

  - Image resizing and normalization
  - Data augmentation for training
  - Support for JPEG, PNG, and WebP formats

- **Feature Extraction**:

  - Deep CNN architectures (ResNet/EfficientNet)
  - ONNX format for cross-platform compatibility
  - TensorRT optimization for GPU inference
  - Output: 512/1024-dimensional embedding vectors

- **Vector Storage & Search**:
  - Qdrant vector database for efficient similarity search
  - HNSW index for fast approximate nearest neighbor search
  - Configurable distance metrics (cosine/euclidean)

### Text Search Pipeline

- **Text Processing & Analysis**:

  - Custom Elasticsearch analyzers:
    - Keyword analyzer with lowercase and ASCII folding
    - Edge NGram analyzer for autocomplete (min_gram: 2, max_gram: 5)
    - Standard analyzer for full-text search
  - Character filters and tokenization
  - Support for Vietnamese text

- **Search Approaches**:

  1. **Autocomplete (Search-as-you-type)**:

     - Edge NGram tokenizer for prefix matching
     - Custom completion suggester
     - Optimized for instant suggestions
     - Minimum 2 characters for suggestions

  2. **Full-Text Search**:
     - Multi-match query across fields:
       - item_name
       - shop_name
     - Fuzzy matching with AUTO fuzziness
     - Custom scoring based on business metrics:
       - Sale rate (discount percentage)
       - Sales volume (>1000 sales bonus)
       - Item price normalization

- **Search Optimization**:

  - Custom scoring template using Elasticsearch scripts
  - Batch indexing for efficient data ingestion
  - Asynchronous search operations
  - Configurable result size
  - Error handling and logging

- **Elasticsearch Features**:
  - Custom index mappings
  - Multiple field types and analyzers
  - Function score queries
  - Script-based scoring
  - Bulk indexing operations

## Technology Stack

### Model Serving

- **NVIDIA Triton Inference Server**:
  - [Triton Server Documentation](./triton_server/README.md)
  - Model versioning and A/B testing
  - Dynamic batching
  - Concurrent model execution
  - GPU optimization with TensorRT
  - Model format conversion pipeline:
    - PyTorch → ONNX → TensorRT

### Infrastructure

- **Containerization**:

  - Docker multi-stage builds
  - Optimized container images
  - Docker Compose for development

- **Orchestration**:

  - Kubernetes deployment
  - [Helm Charts](./helm-charts/README.md) for package management
  - Horizontal Pod Autoscaling
  - Resource management and scaling

- **Monitoring & Logging**:
  - Prometheus metrics
  - Grafana dashboards
  - Distributed tracing
  - Performance monitoring

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/vectornguyen76/search-engine-system.git
```

2. Start the services using Docker Compose:

```bash
docker-compose up -d
```

3. Access the services:

- Image Search UI: http://localhost:8501
- Text Search UI: http://localhost:8502
- Triton Server: http://localhost:8000

## Development

### CI/CD Pipeline

- **Development Environment**:

  - Code linting (Flake8)
  - Unit tests
  - Integration tests

- **Staging Environment**:

  - Performance testing
  - Load testing
  - Security scanning

- **Production Environment**:
  - Blue-green deployment
  - Automated rollback
  - Performance monitoring

### Code Quality

- Flake8 for Python code linting
- Type hints and documentation
- Automated testing in CI/CD pipeline
- Code review process

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
