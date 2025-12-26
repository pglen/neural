import numpy as np

class NeuralNetwork:
    def __init__(self, num_inputs, num_hidden, num_outputs):
        # Initialize the weights with random values
        self.weights_hidden = np.random.randn(num_inputs, num_hidden)
        self.weights_output = np.random.randn(num_hidden, num_outputs)
        # Initialize the biases with zeros
        self.bias_hidden = np.zeros((1, num_hidden))
        self.bias_output = np.zeros((1, num_outputs))

    def forward_propagation(self, inputs):
        # Calculate the activations of the hidden layer
        hidden_layer = np.dot(inputs, self.weights_hidden) + self.bias_hidden
        hidden_layer_activation = self.sigmoid(hidden_layer)

        # Calculate the activations of the output layer
        output_layer = np.dot(hidden_layer_activation, self.weights_output) + self.bias_output
        output = self.sigmoid(output_layer)

        return output

    def sigmoid(self, x):
        # Sigmoid activation function
        return 1 / (1 + np.exp(-x))


# Create a neural network with 2 inputs, 3 hidden units, and 1 output
neural_network = NeuralNetwork(2, 3, 1)

# Define inputs
inputs = np.array([[0.5, 0.2]])

# Perform forward propagation to get the output
output = neural_network.forward_propagation(inputs)

print("Output:", output)

