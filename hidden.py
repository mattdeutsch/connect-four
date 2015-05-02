import defs
import math
from copy import deepcopy

class HiddenLayer():
	"""
	This is simply a hidden neuron of a neuron network. The functions are
	straightforward: forward, backward, update, etc.

	The arguments are the same as in NeuralNet.
	"""
	def __init__(self, inputs, index, init_hweights, init_oweight,
				 init_helig, init_oelig):
		self.inputs = inputs
		self.index = index
		self.h_weights = init_hweights 
		self.o_weight = init_oweight 
		self.h_elig = init_helig
		self.o_elig = init_oelig 

	def forward(self):
		self.output = 0.0
		for i in xrange(defs.NUM_FEATURES):
			self.output += self.inputs[self.index][i] * self.h_weights[i]
		self.output = defs.sigmoid(self.output)

	def backward(self, error):
		self.o_weight += defs.BETA * error * self.o_elig
		for i in xrange(defs.NUM_FEATURES):
			self.h_weights[i] += defs.ALPHA * error * self.h_elig[i]

	def update(self, output):
		diff_sig = output * (1-output)
		self.o_elig = defs.LAMBDA * self.o_elig + diff_sig * self.output
		for i in xrange(defs.NUM_FEATURES):
			self.h_elig[i] = defs.LAMBDA * self.h_elig[i] + diff_sig * \
							 self.o_weight * self.output * (1-self.output) * \
							 self.inputs[self.index][i]

	def get_output(self):
		return self.output

	def get_oweight(self):
		return self.o_weight