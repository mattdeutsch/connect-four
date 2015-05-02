import random 
import math
import neural
import os

""" This file contains several definitions that allow our code to be 
much shorter. Fixed variables for learning, initialization of global
variables for weights for the trainer, and some basic helper fucnctions
such as sigmoid, human_play, cls, etc.
	
These are all pretty straightforward, so we won't bother with many
details here. """
    
INFINITY = 100
NUM_FEATURES = 19
NUM_HIDDEN = 20
ALPHA = 0.1
BETA = 0.05
GAMMA = 0.9
LAMBDA = 0.7
BIAS = 0.5

init_hweights = [0.6, 0.8, 0.7, 0.4, 0.6, 0.6, 0.2, 0.2, 0.2, 0.8, 0.4, 0.4, 0.5, 0.6, 0.6, 0.7, 0.2, 0.2, 0.3, 0.5]
init_oweight = [random.random() for j in xrange(NUM_HIDDEN)]
init_helig = [[random.random() for i in xrange(NUM_FEATURES)] for j in xrange(NUM_HIDDEN)]
init_oelig = [random.random() for j in xrange(NUM_HIDDEN)]

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

def cls():
    os.system(['clear','cls'][os.name == 'nt'])

def print_winner(plyr):
    if (plyr == 1):
        print "X WINS!"
    elif (plyr == -1):
        print "O WINS!"
    else:
        print "IT'S A DRAW!"

def train(b):
    trainer = neural.NeuralNet(b.get_features(),
                               0,
                               init_hweights,
                               init_oweight,
                               init_helig,
                               init_oelig,
                               b.winning())
    trainer.train()

def human_play(b):
    try:
        play = int(raw_input("Where to play? (From 1 to 7): "))
        b.play(play-1)
        b.update_features()
    except ValueError:
        print "Please play an integer from 1 to 7!"
    except UnboundLocalError:
        print "Please play an integer from 1 to 7!"
    except AssertionError:
        print "Please play an integer from 1 to 7!"

def AI_play(b, eng, AI_color):
    (score, move, flag) = eng.getBestMove(b, 2, AI_color)
    if (not flag):
        b.play_random()
    else:
        b.play(move)
    b.update_features()
