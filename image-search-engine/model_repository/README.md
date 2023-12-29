# Converting PyTorch to ONNX and TensorRT

This repository is your guide to converting PyTorch models to ONNX format and then further optimizing them for efficient inference on NVIDIA GPUs using TensorRT.

## Index

- [Converting PyTorch to ONNX](#converting-pytorch-to-onnx)
- [Converting ONNX to TensorRT](#converting-onnx-to-tensorrt)
- [Download PyTorch model in Development Environment](#download-pytorch-model-in-development-environment)
- [Convert model in TensorRT Docker Environment - Release 23.01](#convert-model-in-tensorrt-docker-environment---release-2301)
- [References](#references)

### Converting PyTorch to ONNX

- Export & load ONNX
- Inference using ONNX
- Comparing output and time efficiency between ONNX and PyTorch
- Setting the batch size of input data: explicit batch or implicit batch

### Converting ONNX to TensorRT

- Building & loading TensorRT engine
- Setting the batch size of input data: explicit batch or implicit batch
- Key trtexec options
  - Precision of engine: FP32, FP16
  - optShapes: set the most used input data size of the model for inference
  - minShapes: set the max input data size of the model for inference
  - maxShapes: set the min input data size of the model for inference
- Inference using the TensorRT engine
- Comparing output and time efficiency among TensorRT, ONNX, and PyTorch

### Download PyTorch model in Development Environment

1. **Create Environment and Install Packages**

   ```shell
   conda create -n convert-model python=3.9
   ```

   ```shell
   conda activate convert-model
   ```

   ```shell
   pip install -r requirements.txt
   ```

2. **Download PyTorch model**
   ```shell
   python fetch_model.py
   ```

### Convert model in TensorRT Docker Environment - Release 23.01

Release 23.01 is based on CUDA 12.0.1, which requires NVIDIA Driver release 525 or later. However, if you are running on a data center GPU (for example, T4 or any other data center GPU), you can use NVIDIA driver release 450.51 (or later R450), 470.57 (or later R470), 510.47 (or later R510), 515.65 (or later R515), or 525.85 (or later R525).

1. **Download TensorRT Docker environment**
   ```
   docker pull nvcr.io/nvidia/tensorrt:23.01-py3
   ```
2. **Run TensorRT Docker environment**
   ```
   nvidia-docker run -it --rm -v ./../image-search-engine:/workspace -w /workspace nvcr.io/nvidia/tensorrt:23.01-py3 bash
   ```
3. **Install Packages**
   ```
   cd model_repository
   ```
   ```
   pip install -r requirements.txt
   ```
4. **Convert PyTorch model to ONNX**
   ```
   python pytorch_to_onnx.py --dynamic_axes True --batch_size {batch_size}
   ```
5. **Convert ONNX to TensorRT (FP16)**
   ```
   python onnx_to_tensorrt.py --dynamic_axes True --batch_size {batch_size} --engine_precision FP16
   ```

## References

- [GitHub Repository](https://github.com/qbxlvnf11/convert-pytorch-onnx-tensorrt)
- [TensorRT Container Release Notes](https://docs.nvidia.com/deeplearning/tensorrt/container-release-notes/rel-23-01.html#rel-23-01)
- [Triton Inference Server Issue #2377](https://github.com/triton-inference-server/server/issues/2377)
- [Triton Inference Server Issue #6059](https://github.com/triton-inference-server/server/issues/6059)
