import defs
import math
from copy import deepcopy

class HiddenLayer():
	def __init__(self, inputs, index, init_hweights, init_oweight, init_helig, init_oelig): # inputs: board.get_features()
		self.inputs = inputs
		self.index = index
		self.h_weights = init_hweights # weights for inputs; h_weights[i] = v[i][j]
		self.o_weight = init_oweight # weight for output; o_weight = w[j]
		self.h_elig = init_helig #initial eligibility traces; h_elig[i] = ev[i][j]
		self.o_elig = init_oelig # equivalent to ew; o_elig = ew[j]

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
			self.h_elig[i] = defs.LAMBDA * self.h_elig[i] + diff_sig * self.o_weight * self.output * (1-self.output) * self.inputs[self.index][i]

	def get_output(self):
		return self.output

	def get_oweight(self):
		return self.o_weight