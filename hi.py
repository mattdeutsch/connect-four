import board
import engine
import os 
import random

INFINITY = 100
random.seed()

COLSNUM = 7
ROWSNUM = 6

def negamax(board, depth, color):
    #print "STARTING MINIMAX"
    score = board.get_score()

    if depth == 0:
        return (color * score, None)
    else:
        maxValue = -INFINITY
        maxMove = None

        for i in xrange(0,7):
            c = deepcopy(board)
            if (not board.cannot_play_in(i)):
                oldValue = maxValue
                oldMove = maxMove

                try:
                    c.play(i)
                    (scr, move) = negamax(c, depth - 1, -1*color)
                    scr = -scr

                    #print "scr: {}   -   maxValue: {}".format(scr, maxValue)

                    if scr >= maxValue:
                        maxValue = scr
                        maxMove = i

                    #print "{}{}".format("maxValue: ", maxValue)
                    #print "{}{}".format("maxMove: ", maxMove)

                except ValueError, e:
                    if e.message == "ColumnFull":
                        maxValue = oldValue
                        maxMove = oldMove
                    else:
                        raise ValueError, e

        return (maxValue, maxMove)


class Board(object):
    """docstring for Board"""
    def __init__(self):
        super(Board, self).__init__()
        self.reset()

    def reset(self):
        b = ['.' for c in xrange(0,6)]
        self.cols = [copy(b) for c in xrange(0,7)]
        self.current_player = "X"
        self.fours = {"X": [], "O": []}
        self.init_fours()

    def init_fours(self):
        full_list = []
        # Add the verticals
        for row in xrange(0, 3):
            for col in xrange(0,7):
                full_list.append([(row, col), (row + 1, col), (row + 2, col), (row + 3, col)])
        # Add the horizontals
        for row in xrange(0, 6):
            for col in xrange(0, 4):
                full_list.append([(row, col), (row, col + 1), (row, col + 2), (row, col + 3)])
        # Add the up-rights
        for row in xrange(0, 3):
            for col in xrange(0, 4):
                full_list.append([(row, col), (row + 1, col + 1), (row + 2, col + 2), (row + 3, col + 3)])
        # Add the up-lefts
        for row in xrange(3, 6):
            for col in xrange(0, 4):
                full_list.append([(row, col), (row - 1, col + 1), (row - 2, col + 2), (row - 3, col + 3)])
        for l in full_list:
            print l
        assert(len(full_list) == 69)
        self.fours["X"] = full_list
        self.fours["O"] = deepcopy(full_list)

    def cannot_play_in(self, col):
        return not ('.' in self.cols[col])

    def get_player(self):
        return self.current_player

    def switch_player(self):
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

    def other_player(self):
        other_player = ""
        if self.current_player == "X":
            other_player = "O"
        else:
            other_player = "X"

    def lowest_available(self, col):
        for i, sq in enumerate(self.cols[col]):
            if sq == '.':
                return i

    # 1-indexed cols
    def play(self, col):
        assert 0 <= col < 7
        if (not self.cannot_play_in(col)):
            row = self.lowest_available(col)
            self.cols[col][row] = self.current_player
            print len(self.fours["O"])
            self.remove_fours(col, row)
            print len(self.fours["O"])
            self.switch_player()
        else:
            raise ValueError("ColumnFull")

    def remove_fours(self, col, row):
        other_player = None
        if self.current_player == "X":
            other_player = "O"
        else:
            other_player = "X"
        iterlist = copy(self.fours[other_player])
        for four in iterlist:
            # print ((row, col) in four)
            if (row, col) in four:
                # print "remove " + str(four)
                self.fours[other_player].remove(four)
        # print self.fours[other_player]

    def transpose(self, l):
        # http://stackoverflow.com/a/11387441/2228485
        return [list(i) for i in zip(*l)]

    def display_board(self):
        # mutability makes this more difficult than it probably should be
        # Copy self.cols. Reverse every column
        col_copy = deepcopy(self.cols)
        for c in col_copy:
            c.reverse()
        for r in self.transpose(col_copy):
            print "{} {} {} {} {} {} {}".format(*r)

    def copy_board(self):
        return deepcopy(self.cols)

    def play_random(self):
        x = random.randint(0,6)
        while (self.cannot_play_in(x)):
            x = random.randint(0,6)
        self.play(x)

    def get_score(self):
        score = 0

        for i in xrange(0, COLSNUM - 3):
            for j in xrange(0, ROWSNUM - 3):
                fours = [[],[]]

                for x in xrange (0,10):
                    fours[0].append(0)
                    fours[1].append(0)

                for k in xrange(0,4):
                    for m in xrange(0,4):
                        if (self.cols[i+k][j+m] != "."):
                            if (self.cols[i+k][j+m] == "X"):
                                index = 0
                            elif (self.cols[i+k][j+m] == "O"):
                                index = 1

                            fours[index][k] += 1
                            fours[index][m+4] += 1
                            if (k == m):
                                fours[index][8] += 1
                            elif (k == 3-m):
                                fours[index][9] += 1

                for k in xrange(0,10):
                    if (fours[0][k] == 4):
                        return -1
                    elif (fours[1][k] == 4):
                        return 1
        return score

    def winning(self):
        for four in self.fours[self.other_player()]:
            if (self.cols[(four[0])[1]][(four[0])[0]] ==
               self.cols[(four[1])[1]][(four[1])[0]] ==
               self.cols[(four[2])[1]][(four[2])[0]] ==
               self.cols[(four[3])[1]][(four[3])[0]] ==
               self.other_player):
                print "GAME OVER"
                return True
        return False

    # Heuristics/Features
    # Normalized such that best case for X => 1, best case for 0 => -1
    def fours_left(self):
        return 2 * len(self.fours["X"])/69 - 1

    def fours_left_opponent(self):
        return 2 * (1 - len(self.fours["O"])/69) - 1

    # This should be normalized to something better I think...
    def fours_difference(self):
        return 2 * (len(self.fours["X"]) - len(self.fours["O"]))/69 - 1

    # A helper function.
    def some_in_a_row(self, n, player):
        ns = 0
        for f in self.fours[player]:
            how_many_in = 0
            for (row, col) in f:
                if self.cols[col][row] == player:
                    how_many_in += 1
            if how_many_in >= n:
                ns += 1
        if player == "X":
            return 2 * len(ns)/69 - 1
        else: # player == "O"
            return 2 * (1 - len(ns)/69) - 1

    def important_threes(self):
        return self.some_in_a_row(3, "X")

    def important_threes_opponent(self):
        return self.some_in_a_row(3, "O")

    def important_threes_difference(self):
        return self.important_threes() - self.important_threes_difference()

    def important_twos(self):
        return self.some_in_a_row(2, "X")

    def important_twos_opponent(self):
        return self.some_in_a_row(2, "X")

    def important_twos_difference(self):
        return self.important_twos() - self.important_twos_opponent()

    def present_in(self):
        return self.some_in_a_row(1, "X")

    def opponent_present_in(self):
        return self.some_in_a_row(1, "O")

    def presence_difference(self):
        return self.present_in() - self.opponent_present_in()

def cls():
    os.system(['clear','cls'][os.name == 'nt'])

def multiplayer():
    cls()
    b = board.Board()
    b.display_board
    while(not b.winning()):
        play = input("Where to play?: ")
        b.play(play-1)
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
