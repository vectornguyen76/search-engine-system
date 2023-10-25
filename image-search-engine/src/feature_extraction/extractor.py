import torch
import tritonclient.grpc.aio as grpcclient
from config import settings
from src.utils import LOGGER, decode_img, py_profiling, time_profiling
from torchvision.io import read_image
from torchvision.models import EfficientNet_B3_Weights, efficientnet_b3


class FeatureExtractor:
    def __init__(self):
        """
        Initializes the FeatureExtractor class.

        This class is used to extract features from images using the EfficientNet-B3 model.

        Attributes:
        - device (torch.device): Represents the device (CPU/GPU) where the model will be loaded.
        - weights (EfficientNet_B3_Weights): Specifies the pre-trained weights to be used.
        - model (torch.nn.Module): The loaded EfficientNet-B3 model.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        LOGGER.info(f"Model run on {self.device} device")
        self.weights = EfficientNet_B3_Weights.IMAGENET1K_V1
        self.model = self.load_model()
        self.triton_client = grpcclient.InferenceServerClient(
            url=settings.TRITON_SERVER_URL
        )

    def load_model(self):
        """
        Loads the pre-trained EfficientNet-B3 model.

        Returns:
        - torch.nn.Module: The loaded model.
        """
        # Load the pre-trained model
        model = efficientnet_b3(weights=self.weights)

        # Set the model to evaluation mode
        model.eval()

        # Use a GPU (if available) for inference
        model = model.to(self.device)

        return model

    # @time_profiling
    def preprocess_input(self, image_path):
        """
        Preprocesses the input image for inference.

        Args:
        - image_path (str): The path to the input image.

        Returns:
        - torch.Tensor: Preprocessed image tensor. [1, 3, 300, 300]
        """
        image = read_image(image_path)

        # Initialize the inference transforms
        preprocess = self.weights.transforms(antialias=True)

        # Process RGBA image
        image = image.narrow(0, 0, 3)

        # Apply inference preprocessing transforms
        image = preprocess(image).unsqueeze(0)

        return image

    # @py_profiling
    # @time_profiling
    def extract_feature(self, image_path):
        """
        Extracts features from the input image.

        Args:
        - image_path (str): The path to the input image.

        Returns:
        - numpy.ndarray: Extracted features as a numpy array. (1, 1000)
        """
        image = self.preprocess_input(image_path)

        feature = self.model(image)

        feature = feature.detach().numpy()

        return feature

    async def triton_inference(self, image, model_name, inputs_name, outputs_name):
        inputs = [grpcclient.InferInput(inputs_name, image.shape, datatype="FP32")]
        outputs = [grpcclient.InferRequestedOutput(outputs_name)]

        inputs[0].set_data_from_numpy(image.numpy())

        results = await self.triton_client.infer(
            model_name=model_name, inputs=inputs, outputs=outputs
        )

        feature = results.as_numpy(outputs_name)

        return feature

    # @async_py_profiling
    # @async_time_profiling
    async def triton_extract_feature_onnx(self, image_path):
        image = self.preprocess_input(image_path)

        feature = await self.triton_inference(
            image=image,
            model_name=settings.ONNX_MODEL_NAME,
            inputs_name=settings.MODEL_INPUT_NAME,
            outputs_name=settings.MODEL_OUTPUT_NAME,
        )

        return feature

    # @async_py_profiling
    # @async_time_profiling
    async def triton_extract_feature(self, image_path):
        image = self.preprocess_input(image_path)

        feature = await self.triton_inference(
            image=image,
            model_name=settings.TORCH_MODEL_NAME,
            inputs_name=settings.MODEL_INPUT_NAME,
            outputs_name=settings.MODEL_OUTPUT_NAME,
        )

        return feature

    # @async_py_profiling
    # @async_time_profiling
    async def triton_extract_base64(self, image):
        image = decode_img(image)

        # Initialize the inference transforms
        preprocess = self.weights.transforms(antialias=True)

        # Apply inference preprocessing transforms
        image = preprocess(image).unsqueeze(0)

        feature = await self.triton_inference(
            image=image,
            model_name=settings.ONNX_MODEL_NAME,
            inputs_name=settings.MODEL_INPUT_NAME,
            outputs_name=settings.MODEL_OUTPUT_NAME,
        )

        return feature
