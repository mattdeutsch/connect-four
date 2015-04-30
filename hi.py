import random
import board
import engine
import os
from copy import copy, deepcopy

def cls():
    os.system(['clear','cls'][os.name == 'nt'])

def multiplayer():
    cls()
    b = board.Board()
    b.display_board
    while(not b.winning()):
        play = input("Where to play?: ")
        b.play(play-1)
        cls()
        b.display_board()

def singleplayer():
    cls()
    b = board.Board()
    eng = engine.Engine()
    b.display_board

    while(not b.winning()):
        while(b.get_player() == "X"):
            flag = 0
            while (flag == 0):
                try:
                    play = input("Where to play?: ")
                    flag = 1
                except NameError as e:
                    print "Type in an INTEGER!"
                    flag = 0

            try:
                b.play(play-1)
            except ValueError as e:
                if e.message == "ColumnFull":
                    print "This column is already full. Please pick a different one."
                else:
                    raise ValueError(e)
            except AssertionError:
                print "Type in a valid integer!"
            cls()
            b.display_board()


        if (not b.winning()):
            (score, move, flag) = eng.getBestMove(b, 4)
            if (move is not None):
                try:
                    if (not flag):
                        b.play_random()
                    else:
                        b.play(move)
                except ValueError as e:
                    if e.message == "ColumnFull":
                        pass
                    else:
                        raise ValueError(e)
            else:
                b.play_random()
            print ""
            b.display_board()

def main():
     singleplayer()

if __name__ == "__main__":
    main ()
