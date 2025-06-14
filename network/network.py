import csv
import json
import os
import random
from pathlib import Path

import numpy as np

from util.activation_functions import dsigmoid, sigmoid


class Network(object):
    def __init__(self, sizes, random=False):
        directory_path = Path("parameters")
        if directory_path.exists() and not random:
            self.initialize_from_json(directory_path)
        else:
            self.num_layers = len(sizes)
            self.sizes = sizes
            self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
            self.weights = [
                np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])
            ]

    def initialize_from_json(self, directory_path):
        json_file = [
            file for file in os.listdir(directory_path) if file.endswith(".json")
        ][0]
        with open(directory_path / json_file) as file:
            data = json.load(file)
            self.num_layers = data["num_layers"]
            self.sizes = data["sizes"]
            self.biases = [np.array(bias) for bias in data["biases"]]
            self.weights = [np.array(weight) for weight in data["weights"]]

    def to_dict(self):
        return {
            "num_layers": self.num_layers,
            "sizes": self.sizes,
            "biases": [bias.tolist() for bias in self.biases],
            "weights": [weight.tolist() for weight in self.weights],
        }

    def display(self):
        print("Number of layers: " + str(self.num_layers))
        print("Sizes: " + str(self.sizes))
        print("Biases: " + str(self.biases))
        print("Weights: " + str(self.weights))

    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a

    def cost_derivative(self, output_activations, y):
        return output_activations - y

    def evaluate(self, test_data):
        hits = 0
        misses = 0
        for x, y in test_data:
            result = self.feedforward(x)
            for i in range(result.size):
                for j in range(result[0].size):
                    if result[i][j] > 0.7 and y[i][j] == 1:
                        hits += 1
                    elif result[i][j] > 0.7 and y[i][j] == 0:
                        misses += 1
        if hits + misses == 0:
            return 0
        percentage_hit = hits / (hits + misses)
        directory_path = Path("parameters")
        directory_path.mkdir(exist_ok=True)
        self.save_parameters_to_json(
            f"{directory_path / str(round(percentage_hit * 100))}.json"
        )
        return percentage_hit

    def backprop(self, x, y):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        activation = x
        activations = [x]
        zs = []
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        delta = self.cost_derivative(activations[-1], y) * dsigmoid(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        for layer in range(2, self.num_layers):
            z = zs[-layer]
            sp = dsigmoid(z)
            delta = np.dot(self.weights[-layer + 1].transpose(), delta) * sp
            nabla_b[-layer] = delta
            nabla_w[-layer] = np.dot(delta, activations[-layer - 1].transpose())
        return (nabla_b, nabla_w)

    def update_mini_batch(self, mini_batch, eta):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [
            w - (eta / len(mini_batch)) * nw for w, nw in zip(self.weights, nabla_w)
        ]
        self.biases = [
            b - (eta / len(mini_batch)) * nb for b, nb in zip(self.biases, nabla_b)
        ]

    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        if test_data:
            n_test = len(test_data)
        n = len(training_data)
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k : k + mini_batch_size]
                for k in range(0, n, mini_batch_size)
            ]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                print(
                    "Epoch {0}: {1} / {2}".format(j, self.evaluate(test_data), n_test)
                )
            else:
                print("Epoch {0} complete".format(j))
        self.select_best_epoch()

    def select_best_epoch(self):
        directory_path = Path("parameters")
        max_accuracy = 0
        for file in os.listdir(directory_path):
            if file.endswith(".json"):
                accuracy = int(file.split(".")[0])
                if accuracy > max_accuracy:
                    max_accuracy = accuracy
        for file in os.listdir(directory_path):
            if file.endswith(".json"):
                accuracy = int(file.split(".")[0])
                if accuracy != max_accuracy:
                    os.remove(directory_path / file)

    def save_biases_and_weights_to_csv(self, filename):
        with open(filename, mode="w", newline="") as file:
            csv_writer = csv.writer(file)
            for bias in self.biases:
                bias_record = [str(value) for value in bias]
                csv_writer.writerow(bias_record)
            for weight in self.weights:
                weight_record = [str(value) for value in weight]
                csv_writer.writerow(weight_record)

    def save_parameters_to_json(self, filename):
        with open(filename, mode="w") as file:
            json.dump(self.to_dict(), file, indent=4)
