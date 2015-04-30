from copy import copy, deepcopy

INFINITY = 100

# This defines the core of this AI, the PVS algorithm (Principal Variation Search).
# It is very similar to Minimax with Alpha-Beta Pruning, but can be up to 10% more efficient
# and is simpler to code, since we are using a variation of Negamax (equivalent to
# Minimax on a zero-sum game).

class Engine(object):
    # Main recursion.
    def PVS(self, board, depth, alpha, beta, color):
        score = board.get_score()
        maxValue = -INFINITY

        if depth == 0 or score == 1:
            return (color * score)
        else:
            for i in xrange(0,7):
                c = deepcopy(board)
                if (not board.cannot_play_in(i)):
                    c.play(i)
                    if (i == 0):
                        scr = -self.PVS(c, depth - 1, -beta, -alpha, -color)
                    else:
                        scr = -self.PVS(c, depth - 1, -alpha-1, -alpha, -color)
                        if (alpha < scr < beta):
                            scr = -self.PVS(c, depth - 1, -beta, -scr, -color)

                    alpha = max(alpha, scr)

                    if (alpha >= beta):
                        break
            return alpha

    # On the first node, we should keep track of the move.
    def getBestMove(self, board, depth):
        maxValue = -INFINITY
        maxMove = None

        alpha = -INFINITY
        beta = INFINITY

        flag = False

        for i in xrange(0,7):
            c = deepcopy(board)
            if (not board.cannot_play_in(i)):
                c.play(i)
                scr = -self.PVS(c, depth - 1, alpha, beta, 1)

                if scr == -1:
                    flag = True

                if (scr >= alpha):
                    alpha = scr
                    maxMove = i

                if (alpha >= beta):
                    return (alpha, maxMove, flag)
        return (alpha, maxMove, flag)
