import defs
import hidden
from copy import deepcopy

class NeuralNet(object):
    def __init__(self, inputs, index, init_hweights, init_oweight, init_helig, init_oelig, final): # inputs: board.get_features()
        self.inputs = inputs
        self.final = final # 1 if White won, -1 if Black won
        self.num_states = len(inputs)
        self.index = index
        self.init_hweights = init_hweights # weights for inputs; equivalent to v
        self.init_oweight = init_oweight # weight for output; equivalent to w
        self.init_helig = init_helig #initial eligibility traces; equivalent to ev
        self.init_oelig = init_oelig # equivalent to ew
        self.error = 0.0

        for i in xrange(self.num_states):
            self.inputs[self.index].append(defs.BIAS)

        self.hid_neurons = []

        for i in xrange(defs.NUM_HIDDEN):
            self.hid_neurons.append(hidden.HiddenLayer(self.inputs, self.index, self.init_hweights[i], self.init_oweight[i], self.init_helig[i], self.init_oelig[i]))

        self.forward()
        self.old_output = self.output
        self.update()

    def forward(self):
        for neuron in self.hid_neurons:
            neuron.forward()   

        self.output = 0.0
        for i in xrange(defs.NUM_HIDDEN):
            self.output += self.hid_neurons[i].get_output() * self.hid_neurons[i].get_oweight()

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
            next = NeuralNet(self.inputs, self.index+1, self.init_hweights, self.init_oweight, self.init_helig, self.init_oelig, self.final)
            reward = next.train()

        self.error = reward + defs.GAMMA * self.output - self.old_output
        self.backward()
        self.forward()
        self.old_output = self.output
        self.update()
        return reward
