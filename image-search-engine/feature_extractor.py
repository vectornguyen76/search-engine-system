import torch
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
        self.weights = EfficientNet_B3_Weights.IMAGENET1K_V1
        self.model = self.load_model()

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

    def preprocess_input(self, image_path):
        """
        Preprocesses the input image for inference.

        Args:
        - image_path (str): The path to the input image.

        Returns:
        - torch.Tensor: Preprocessed image tensor.
        """
        image = read_image(image_path)

        # Initialize the inference transforms
        preprocess = self.weights.transforms(antialias=True)

        # Process RGBA image
        image = image.narrow(0, 0, 3)

        # Apply inference preprocessing transforms
        image = preprocess(image).unsqueeze(0)

        return image

    def extract_feature(self, image_path):
        """
        Extracts features from the input image.

        Args:
        - image_path (str): The path to the input image.

        Returns:
        - numpy.ndarray: Extracted features as a numpy array.
        """
        image = self.preprocess_input(image_path)

        feature = self.model(image)

        feature = feature.detach().numpy()

        return feature
