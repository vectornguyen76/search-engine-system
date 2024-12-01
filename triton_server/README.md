# Triton Model Conversion Guide

This guide explains how to convert PyTorch models to ONNX and TensorRT formats for use with NVIDIA Triton Inference Server.

## Directory Structure

```
model_repository/
├── efficientnet_b3/           # PyTorch model
│   ├── 1/
│   │   └── model.pt
│   └── config.pbtxt
├── efficientnet_b3_onnx/      # ONNX model
│   ├── 1/
│   │   └── model.onnx
│   └── config.pbtxt
└── efficientnet_b3_trt/       # TensorRT model
    ├── 1/
    │   └── model.plan
    └── config.pbtxt
```

## Quick Start

### 1. Set Up Development Environment

```bash
# Create and activate conda environment
conda create -n triton-convert python=3.9
conda activate triton-convert

# Install dependencies
pip install -r requirements.txt

# Download and save PyTorch model
python fetch_model.py
```

### 2. Convert Models Using TensorRT Docker

```bash
# Pull TensorRT container
docker pull nvcr.io/nvidia/tensorrt:23.01-py3

# Run container with mounted volume
docker run -it --rm --gpus all \
  -v $(pwd):/workspace \
  -w /workspace \
  nvcr.io/nvidia/tensorrt:23.01-py3

# Convert PyTorch to ONNX
python pytorch_to_onnx.py --dynamic_axes True --batch_size 32

# Convert ONNX to TensorRT
python onnx_to_tensorrt.py \
  --dynamic_axes True \
  --batch_size 32 \
  --engine_precision FP16
```

## Conversion Details

### PyTorch to ONNX Conversion

- Supports dynamic batch sizes
- Preserves model parameters and weights
- Validates numerical accuracy between PyTorch and ONNX outputs
- Configurable options:
  - `--dynamic_axes`: Enable/disable dynamic batch sizing
  - `--batch_size`: Set batch size for conversion
  - `--opset_version`: ONNX opset version (default: 11)

### ONNX to TensorRT Conversion

- Optimizes model for NVIDIA GPUs
- Supports FP16/FP32 precision
- Configurable batch size ranges:
  - `--min_engine_batch_size`: Minimum batch size
  - `--opt_engine_batch_size`: Optimal batch size
  - `--max_engine_batch_size`: Maximum batch size

## Model Configurations

Each model format has its own configuration in `config.pbtxt`:

- **PyTorch Model**: Uses `pytorch_libtorch` backend
- **ONNX Model**: Uses `onnxruntime_onnx` backend
- **TensorRT Model**: Uses `tensorrt_plan` backend

All models support:

- Dynamic batching
- GPU execution
- Multiple model instances
- Configurable input/output shapes

## System Requirements

- NVIDIA GPU with compute capability 6.0+
- NVIDIA Driver 525+ (or 450.51+ for data center GPUs)
- Docker with NVIDIA Container Toolkit
- CUDA 12.0.1 (via TensorRT container)

## Troubleshooting

Common issues and solutions:

- Memory errors: Reduce batch size or model precision
- Conversion failures: Check input shapes and ONNX opset compatibility
- Performance issues: Tune batch sizes and instance counts

## References

- [TensorRT Container Documentation](https://docs.nvidia.com/deeplearning/tensorrt/container-release-notes/rel-23-01.html)
- [Triton Inference Server Documentation](https://github.com/triton-inference-server/server)
- [ONNX Model Zoo](https://github.com/onnx/models)
