from os import path, listdir
from random import choice
from tensorflow.keras.applications import resnet
from PIL import Image
import numpy as np


class ImagePreparation:
    def __init__(self, uploads_path, target_shape: tuple = None):
        self.uploads_path = uploads_path

        if target_shape is None:
            self.target_shape = (200, 200)

        else:
            self.target_shape = target_shape

    def get_photos_set(self, student_id, random_student_id, image_path, uploaded_file):
        images = self.load_image(student_id, random_student_id, image_path, uploaded_file)
        x_arrays = self.preprocess_image(*images)

        return x_arrays

    @staticmethod
    def load_image(student_id, random_student_id, image_path, uploaded_file):
        uploaded_img = Image.open(image_path + uploaded_file)

        student_path = path.join(image_path, student_id)
        student_img = Image.open(
            student_path + choice([x for x in listdir(student_path)]))

        random_student_path = path.join(image_path, random_student_id)
        random_student_img = Image.open(
            random_student_path + choice([x for x in listdir(random_student_path)])
        )

        return uploaded_img, student_img, random_student_img

    def preprocess_image(self, uploaded_img: Image.Image, student_img: Image.Image, random_student_img: Image.Image):
        uploaded_img = uploaded_img.resize(self.target_shape)
        student_img = student_img.resize(self.target_shape)
        random_student_img = random_student_img.resize(self.target_shape)

        uploaded_arr = np.array(uploaded_img, dtype="utf8")
        student_arr = np.array(student_img, dtype="utf8")
        random_student_arr = np.array(random_student_img, dtype="utf8")

        return uploaded_arr, student_arr, random_student_arr
