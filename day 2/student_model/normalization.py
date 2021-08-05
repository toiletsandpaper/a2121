import matplotlib.pyplot as plt
import numpy as np
import os
import random
from PIL import Image
from tensorflow.keras.applications import resnet


class ImagePreparation:
    def __init__(self, uploads_path, target_shape: tuple = None):
        self.uploads_path = uploads_path

        if target_shape is None:
            self.target_shape = (200, 200)

        else:
            self.target_shape = target_shape

    def load_image(self, student_id, image_path):
        img = image_path

    def preprocess_image(self, image: Image.Image):
        image = image.resize(self.target_shape)
