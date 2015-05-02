from copy import copy, deepcopy
import defs

class Engine(object):
    """
    docstring for Engine

    This defines the core of this AI, the PVS algorithm (Principal Variation 
    Search). It is very similar to Minimax with Alpha-Beta Pruning, but can 
    be up to 10 percent more efficient and is simple to code. This also
    uses the fact that Connect 4 is a zero-sum game.

    Methods:

    PVS: board -> depth -> alpha -> beta -> color -> machine_weights -> float
        This method is the main recursion in this algorithm. Although fairly
        simple to code, it is not as easy to comprehend fully. It takes a board,
        a depth of search, parameters alpha and beta that serve to cut off 
        impossible search trees and color, which serves to switch between players,
        using the fact that Connect 4 in a zero-sum game.

        Notice that this uses board.get_score() as an evaluation function
        to tell which of the nodes in terminal depth is the best one to use.

        Alpha-Beta are the same as in Alpha-Beta Pruning, except for the fact
        that we use a "quicker" search with bounds (-alpha-0.1, -alpha) to check
        whether or not we should fully search the tree. This way, it cuts off
        even more cases.

        machine_weights is just a bool to consider or not the weights trained, 
        or the human weights previously set up.

    getBestMove: board -> depth -> machine_weights -> (float, float, bool)
        This method is very similar to the main loop described above, but it has
        to get the best move as well, so that our AI knows which move to play. 
        Flag is true if the move is necessary - namely, if it is an immediate threat.
    """

    def PVS(self, board, depth, alpha, beta, color, machine_weights):
        # Gets score for this current board, and sets the maxValue to -INF.
        score = board.get_score(machine_weights)
        maxValue = - defs.INFINITY

        # If we are in depth 0 or if we found a win opportunity, then 
        # we return the score (weighted by color depending on the player).
        # Otherwise, it goes into the main PVS loop.
        if depth == 0 or score == defs.INFINITY:
            return (color * score)
        else:
            for i in board.playable():
                c = deepcopy(board)
                c.play(i)
                if (i == 0):
                    scr = -self.PVS(c, depth - 1, -beta, -alpha, 
                                    -color, machine_weights)
                else:
                    scr = -self.PVS(c, depth - 1, -alpha-0.1, -alpha, 
                                    -color, machine_weights)
                    if (alpha < scr < beta):
                        scr = -self.PVS(c, depth - 1, -beta, -scr, 
                                        -color, machine_weights)

                alpha = max(alpha, scr)

                if (alpha >= beta):
                    break
            return alpha

    # On the first node, we should keep track of the move.
    def getBestMove(self, board, depth, plyr, machine_weights):
        maxValue = - defs.INFINITY
        maxMove = None

        # Initial values for alpha and beta.
        alpha = - defs.INFINITY
        beta = defs.INFINITY

        flag = False

        for i in board.playable():
            c = deepcopy(board)
            c.play(i)
            scr = -self.PVS(c, depth - 1, alpha, beta, plyr, machine_weights)

            if scr == -defs.INFINITY or scr == defs.INFINITY:
                flag = True

            if (scr >= alpha):
                alpha = scr
                maxMove = i

            if (alpha >= beta):
                return (alpha, maxMove, flag)
        return (alpha, maxMove, flag)