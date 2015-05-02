import defs
import hidden
from copy import deepcopy

class NeuralNet(object):
    """
    This is the neural network. It takes as arguments the board states,
    an index corresponding to each board state, an initial weight matrix
    for the hidden neurons, an initial weight vector for the output neuron,
    and the initial eligibility traces. Instead of using Backpropagation,
    the TD-Gammon algorithm allows us to derive an explicit formula for this.

    The methods here are fairly straightforward: forward in the network, backward,
    update and train. In train, we use the rewards as the outputs of the next 
    functions, as described in the writeup and cited in the TD-Gammon writeup
    by Tesauro.
    """

    def __init__(self, inputs, index, init_hweights, init_oweight, 
                init_helig, init_oelig, final):
        self.inputs = inputs
        self.final = final 
        self.num_states = len(inputs)
        self.index = index
        self.init_hweights = init_hweights
        self.init_oweight = init_oweight
        self.init_helig = init_helig 
        self.init_oelig = init_oelig
        self.error = 0.0

        for i in xrange(self.num_states):
            self.inputs[self.index].append(defs.BIAS)

        self.hid_neurons = []

        for i in xrange(defs.NUM_HIDDEN):
            self.hid_neurons.append(
                hidden.HiddenLayer(self.inputs, self.index,
                self.init_hweights[i], self.init_oweight[i], 
                self.init_helig[i], self.init_oelig[i])
                )

        self.forward()
        self.old_output = self.output
        self.update()

    def forward(self):
        for neuron in self.hid_neurons:
            neuron.forward()   

        self.output = 0.0
        for i in xrange(defs.NUM_HIDDEN):
            self.output += self.hid_neurons[i].get_output() * \
                           self.hid_neurons[i].get_oweight()

        self.output += defs.BIAS
        self.output = defs.sigmoid(self.output)

    def backward(self):
        for neuron in self.hid_neurons:
            neuron.backward(self.error)

    def update(self):
        for neuron in self.hid_neurons:
            neuron.update(self.output)

    def train(self):
        self.forward()

        if (self.index == self.num_states)-1:
            reward = self.final
        else:
            next = NeuralNet(self.inputs, self.index+1, self.init_hweights,
                             self.init_oweight, self.init_helig, 
                             self.init_oelig, self.final)
            reward = next.train()

        self.error = reward + defs.GAMMA * self.output - self.old_output
        self.backward()
        self.forward()
        self.old_output = self.output
        self.update()
        return reward
