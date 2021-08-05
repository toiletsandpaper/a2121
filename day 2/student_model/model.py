import matplotlib.pyplot as plt
import numpy as np
import os
import random
import tensorflow as tf
from pathlib import Path
from tensorflow.keras import applications
from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import optimizers
from tensorflow.keras import metrics
from tensorflow.keras import Model
from tensorflow.keras.applications import resnet
from os import path


class StudentSiameseModel:
    def __init__(self):
        self.target_shape = (200, 200)

        self.siamese_model = None
        self.embedding = None
        self.siamese_network = None

        self.weights_name = "a2121_schoolx_siamese_weights.h5"
        self.similarity_dot = .6

    def build_model(self):
        base_cnn = resnet.ResNet50(
            weights="imagenet", input_shape=self.target_shape + (3,), include_top=False
        )

        flatten = layers.Flatten()(base_cnn.output)
        dense1 = layers.Dense(512, activation="relu")(flatten)
        dense1 = layers.BatchNormalization()(dense1)
        dense2 = layers.Dense(256, activation="relu")(dense1)
        dense2 = layers.BatchNormalization()(dense2)
        output = layers.Dense(256)(dense2)

        self.embedding = Model(base_cnn.input, output, name="Embedding")

        trainable = False
        for layer in base_cnn.layers:
            if layer.name == "conv5_block1_out":
                trainable = True
            layer.trainable = trainable

        anchor_input = layers.Input(name="anchor", shape=self.target_shape + (3,))
        positive_input = layers.Input(name="positive", shape=self.target_shape + (3,))
        negative_input = layers.Input(name="negative", shape=self.target_shape + (3,))

        distances = self.DistanceLayer()(
            self.embedding(resnet.preprocess_input(anchor_input)),
            self.embedding(resnet.preprocess_input(positive_input)),
            self.embedding(resnet.preprocess_input(negative_input)),
        )

        self.siamese_network = Model(
            inputs=[anchor_input, positive_input, negative_input], outputs=distances
        )

        self.siamese_model = self.SiameseModel(self.siamese_network)
        self.siamese_model.compile(optimizer=optimizers.Adam(0.0001))
        self.siamese_model.built = True
        self.siamese_model.load_weights(
            path.join(path.dirname(__file__), self.weights_name)
        )

        return self.embedding, self.siamese_network, self.siamese_model

    def predict(self, uploaded_image, student_image, random_student_image, similarity_dot=None):
        if any([self.embedding is None, self.siamese_network is None, self.siamese_model is None]):
            raise ImportError("There is no preloaded weights, turns back.")

        if similarity_dot is None:
            similarity_dot = self.similarity_dot

        anchor = np.array([uploaded_image])
        positive = np.array([student_image])
        negative = np.array([random_student_image])

        anchor_embedding, positive_embedding, negative_embedding = (
            self.embedding(resnet.preprocess_input(anchor)),
            self.embedding(resnet.preprocess_input(positive)),
            self.embedding(resnet.preprocess_input(negative)),
        )

        cosine_similarity = metrics.CosineSimilarity()

        positive_similarity = cosine_similarity(anchor_embedding, positive_embedding)
        negative_similarity = cosine_similarity(anchor_embedding, negative_embedding)

        print(positive_similarity.numpy(), negative_similarity.numpy())

        if positive_similarity.numpy() > negative_similarity.numpy() and positive_similarity.numpy() > similarity_dot:
            return True

        else:
            return False

    class DistanceLayer(layers.Layer):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        @staticmethod
        def call(anchor, positive, negative):
            ap_distance = tf.reduce_sum(tf.square(anchor - positive), -1)
            an_distance = tf.reduce_sum(tf.square(anchor - negative), -1)
            return ap_distance, an_distance

    class SiameseModel(Model):
        def __init__(self, siamese_network, margin=0.5):
            super().__init__()
            self.siamese_network = siamese_network
            self.margin = margin
            self.loss_tracker = metrics.Mean(name="loss")

        def call(self, inputs):
            return self.siamese_network(inputs)

        def train_step(self, data):
            with tf.GradientTape() as tape:
                loss = self._compute_loss(data)

            gradients = tape.gradient(loss, self.siamese_network.trainable_weights)

            self.optimizer.apply_gradients(
                zip(gradients, self.siamese_network.trainable_weights)
            )

            self.loss_tracker.update_state(loss)
            return {"loss": self.loss_tracker.result()}

        def test_step(self, data):
            loss = self._compute_loss(data)

            self.loss_tracker.update_state(loss)
            return {"loss": self.loss_tracker.result()}

        def _compute_loss(self, data):
            ap_distance, an_distance = self.siamese_network(data)

            loss = ap_distance - an_distance
            loss = tf.maximum(loss + self.margin, 0.0)
            return loss

        @property
        def metrics(self):
            return [self.loss_tracker]
