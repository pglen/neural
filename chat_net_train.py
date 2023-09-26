import numpy as np
import sys

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
        #print("x", x)
        # Sigmoid activation function
        #return
        #ss = np.tanh(x * 3)
        #ss = np.fabs(x)
        ss = 1 / (1 + np.exp(-x))
        #print("xx", x, "ss", ss)
        return ss

    def train(self, inputs, targets, num_epochs, learning_rate):
        cnt = 0
        for epoch in range(num_epochs):
            # Forward propagation
            hidden_layer = np.dot(inputs, self.weights_hidden) + self.bias_hidden
            hidden_layer_activation = self.sigmoid(hidden_layer)
            output_layer = np.dot(hidden_layer_activation, self.weights_output) + self.bias_output
            output = self.sigmoid(output_layer)

            # Backpropagation
            output_error = targets - output
            output_gradient = output_error * self.sigmoid_derivative(output)

            hidden_error = np.dot(output_gradient, self.weights_output.T)
            hidden_gradient = hidden_error * self.sigmoid_derivative(hidden_layer_activation)

            # Update weights and biases

            if cnt % 4 == 0:
                self.weights_output += np.dot(hidden_layer_activation.T, output_gradient) * learning_rate
            elif cnt % 4 == 1:
                self.bias_output += np.sum(output_gradient, axis=0, keepdims=True) * learning_rate
            if cnt % 4 == 2:
                self.weights_hidden += np.dot(inputs.T, hidden_gradient) * learning_rate

            #else:
            #    self.bias_hidden += np.sum(hidden_gradient, axis=0, keepdims=True) * learning_rate

            cnt += 1


    def sigmoid_derivative(self, x):
        # Derivative of the sigmoid function
        #return x * (1 - x)
        return x #+ .001

eee=int((sys.argv[1]))

#print("eee", eee)

def parr(arr):
    strx = ""
    for aa in arr:
        strx += " ["
        for bb in aa:
            strx += " %.3f" % bb
        strx += "]"
    return strx

# Create a neural network with 2 inputs, 3 hidden units, and 1 output
neural_network = NeuralNetwork(2, 3, 1)

# Define inputs and targets for   training
inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
targets = np.array([[0], [1], [1], [1]])

inputs2 = np.array([[1, 1], [0, 0], [0 , 0], [0, 0]])
targets2 = np.array([[1], [0], [0], [0]])

# Train the neural network
neural_network.train(inputs, targets, num_epochs=eee, learning_rate=1)
#neural_network.train(inputs2, targets2, num_epochs=eee, learning_rate=0.5)

# Test the trained network
output = neural_network.forward_propagation(inputs)
#print("Inputs:")
#print(parr(inputs))
print("Output:")
print(parr(output))
print(parr(targets))
#print()

#output2 = neural_network.forward_propagation(inputs2)
#print("Inputs:")
#print(parr(inputs2))
#print("Output2:")
#print(parr(output2))
#print(parr(targets2))

