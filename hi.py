import random
import board
import engine
import os
from copy import copy, deepcopy

def cls():
    os.system(['clear','cls'][os.name == 'nt'])

def which_mode():
    cls()
    mode = ""
    while not("s" in mode or "m" in mode):
        mode = raw_input("Singleplayer vs. the computer or multiplayer? (s/m):" )
    if "s" in mode:
        return singleplayer()
    return multiplayer()

def multiplayer():
    cls()
    b = board.Board()
    b.display_board
    while(not b.winning()):
        try:
            play = int(raw_input("Where to play? (From 1 to 7): "))
        except ValueError:
            print "Please play an integer from 1 to 7!"
        try:
            b.play(play-1)
        except UnboundLocalError:
            print "Please play an integer"
        except ValueError:
            print "Please pick an integer."
        except AssertionError:
            print "Please pick a number from 1 to 7"
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
                    play = int(raw_input("Where to play?: "))
                    flag = 1
                except ValueError:
                    print "Please play an integer from 1 to 7!"
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
     which_mode()

if __name__ == "__main__":
    main ()
