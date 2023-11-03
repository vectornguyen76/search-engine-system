# Converting PyTorch to ONNX and TensorRT

This repository provides a guide and code for converting PyTorch models to ONNX format and subsequently converting ONNX models to TensorRT for more efficient inference on NVIDIA GPUs. This README document will help you understand the project's structure and how to use it effectively.

## Table of Contents

1. [Converting PyTorch to ONNX](#converting-pytorch-to-onnx)

   - Export & load ONNX
   - Inference using ONNX
   - Comparing output and time efficiency between ONNX and PyTorch
   - Setting the batch size of input data: explicit batch or implicit batch

2. [Converting ONNX to TensorRT](#converting-onnx-to-tensorrt)

   - Building & loading TensorRT engine
   - Setting the batch size of input data: explicit batch or implicit batch
   - Key trtexec options
     - Precision of engine: FP32, FP16
     - optShapes: set the most used input data size of the model for inference
     - minShapes: set the max input data size of the model for inference
     - maxShapes: set the min input data size of the model for inference
   - Inference using the TensorRT engine
   - Comparing output and time efficiency among TensorRT, ONNX, and PyTorch

3. [Environment Development](#environment-development)

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

   2. **Run**

      ```shell
      python fetch_model.py
      ```

      ```shell
      python pytorch_to_onnx.py
      ```

      ```shell
      python onnx_to_tensorrt.py
      ```

## References

- [GitHub Repository](https://github.com/qbxlvnf11/convert-pytorch-onnx-tensorrt)
- [Triton Inference Server Issue #2377](https://github.com/triton-inference-server/server/issues/2377)
- [Triton Inference Server Issue #6059](https://github.com/triton-inference-server/server/issues/6059)
- [NVIDIA TensorRT Release Notes](https://docs.nvidia.com/deeplearning/tensorrt/container-release-notes/rel-23-01.html#rel-23-01)

Please follow the sections above to understand how to use the provided code and to perform the PyTorch to ONNX and ONNX to TensorRT conversions. For any issues or questions, refer to the provided references or the GitHub repository for further assistance.
