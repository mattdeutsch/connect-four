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
NUM_FEATURES = 9
NUM_HIDDEN = 20
ALPHA = 0.1
BETA = 0.05
GAMMA = 0.9
LAMBDA = 0.7
BIAS = 0.2

random.seed()

init_hweights = [[random.random() for i in xrange(NUM_FEATURES)] for j in xrange(NUM_HIDDEN)]
init_oweight = [random.random() for j in xrange(NUM_HIDDEN)]
init_helig = [[random.random() for i in xrange(NUM_FEATURES)] for j in xrange(NUM_HIDDEN)]
init_oelig = [random.random() for j in xrange(NUM_HIDDEN)]
human_weights = [random.random() for i in xrange(NUM_FEATURES)]

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
    except ValueError as e:
        if e.message == "ColumnFull":
            print "This column is full."
    except UnboundLocalError:
        print "Please play an integer from 1 to 7!"
    except AssertionError:
        print "Please play an integer from 1 to 7!"

def AI_play(b, eng, AI_color, code, depth, first):
    if code == 1:
        (score, move, flag) = eng.getBestMove(b, depth, AI_color, True)
        if (not flag and first):
            b.play_random()
        else:
            b.play(move)
        b.update_features()

    elif code == 2:
        (score, move, flag) = eng.getBestMove(b, depth, AI_color, False)
        b.play(move)
        b.update_features()

    elif code == 3:
        (score, move, flag) = eng.getBestMove(b, depth, AI_color, True)
        if (not flag and (first or random.random() < 0.1)):
            b.play_random()
        else:
            b.play(move)
        b.update_features()
