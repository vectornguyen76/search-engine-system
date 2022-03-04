"""
Write by Quang Van
"""
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
import tensorflow.keras as keras

class FeatureExtractor:
    def __init__(self):
        base_model = ResNet50(weights="weight_resnet50.h5", include_top=False)
        x = base_model.output
        x = keras.layers.GlobalAveragePooling2D()(x)
        self.model = keras.Model(inputs=base_model.input, outputs=x)
        
    def extract(self, img):
        
        x = preprocess_input(img)  # Subtracting avg values for each pixel
        feature = self.model.predict(x)  # (1, 2048)
        return feature # Normalize
