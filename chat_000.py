import math

class Neuron:
    def __init__(self, num_inputs):
        # Initialize weights randomly
        self.weights = [0.0] * num_inputs
        self.bias = 0.0

    def activate(self, inputs):
        # Calculate the weighted sum of inputs
        weighted_sum = 0.0
        for i in range(len(inputs)):
            weighted_sum += inputs[i] * self.weights[i]

        # Add bias
        weighted_sum += self.bias

        # Apply activation function (here, we use sigmoid)
        activation = self.sigmoid(weighted_sum)

        return activation

    def sigmoid(self, x):

        print(x, math.exp(-x))
        # Sigmoid activation function
        return 1 / (1 + math.exp(-x))


# Create a neuron with 3 inputs
neuron = Neuron(3)

# Define inputs
inputs = [0.5, -0.2, 0.1]

# Activate the neuron
output = neuron.activate(inputs)

print("Output:", output)

