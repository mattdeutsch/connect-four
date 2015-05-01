from copy import copy, deepcopy
import random

class Problem(object):
	"""
	Generalization of the idea of a 4 in a row. Contains the data of how the
	opponent can deal with the threat.
	"""
	def __init__(self, four):
		self.four = four
		self.solutions = []

	def add_solution(self, s):
		self.solutions.append(s)

	# Required in order to have it be a key in a dict.
	def __hash__(self):
		return str(self.four)

	def __eq__(self, other):
		return self.four == other.four

class Solution(object):
	"""
	A solution is a method by which p2 can provably attain a square, blocking a white threat.
	Each solution is due to one of nine defined rules.
	Many solutions solve more than one threat - i.e., two threats which
	need the same square to be completed, or one solution which guarantees
	p2 two squares.
	We must track which squares the rule relies upon so that we can combine
	the solution with other solutions involving the same squares later on
	in the proper manner.
	"""
	def __init__(self, rule, squares, columns, threats):
		self.rule = rule
		self.squares = squares
		self.columns = columns
		# We threat threats as a list of four in a rows. May change this later.
		self.threats = threats

	def compatible(self, other):
		# Wow this is not simple. TODO.
		pass

	# Required in order to have it be the key in a dict.
	def __hash__(self):
		return (self.rule, str(self.squares))

	def __eq__(self, other):
		return (self.rule == other.rule) and (self.squares == other.squares)
		

class Perfect(object):
	"""Implements the perfect algorithm."""

	def getBestMove(self, board, player):
		# Apply the rules to your situation.
		# If white, is the situation already a draw? Then it doesn't matter.
		# If black, is the situation already a loss? Then it doesn't matter.
		# If it's white's turn, check to see if draw for black.
		#   yes -> doesn't matter, play randomly.
		#   no  -> Evaluate each potential next move, and black's potential follow ups
		#          and see what leads to draws. If any follow-up move leads to a draw,
		#          then we don't play that move. If all follow-up moves lead to potential draws, then we cry (i.e. play randomly).
		# If it's black's turn, check each move and see if it results in a draw.
		#   yes -> Play one of these moves.
		#   no  -> Doesn't matter, play randomly.
		if player = "X":
			if self.p2_can_draw(board):
				# May be replaced later by an actually random place on the board to play.
				return None
			else:
				good_choices = range(0, 7)
				for i in xrange(0, 7):
					c = deepcopy(board)
					if board.can_play_in(i):
						c.play(i)
						for j in xrange(0, 7):
							if board.can_play_in(j):
								c.play(j)
								# Do not make any move that black can force a draw from.
								if self.p2_can_draw(c):
									good_choices.remove(i)
				return random.choice(good_choices)

	def p2_can_draw(self, board):
		# The "X" here is not a mistake.
		# We check for p2's draws on p1's turn intentionally.
		assert board.current_player == "X"
		solutions = self.create_solution_list(board)
		problems = self.create_problem_list(board, solutions)
		self.refine_solutions(solutions, problems)
		# The graph is a dictionary with keys of type Solution or Problem
		#   and values of type set.
		graph = {}
		# this may be the bottleneck of the algorithm
		for s1 in solutions:
			graph[s1] = set(s1.threats)
			for s2 in solutions:
				if not s1.compatible(s2):
					graph[s1].add(s2)
		self.determine_solution_set(graph, set())



	def create_solution_list(self, board):
		"""
		We check for instances of each of our 9 rules.
		Whenever we find one, we add it to the list.
		See section 6 of http://www.informatik.uni-trier.de/~fernau/DSL0607/Masterthesis-Viergewinnt.pdf
		"""
		solution_list = []
		solution_list += self.claimevens(board)
		solution_list += self.baseinverses(board)
		solution_list += self.verticals(board)
		solution_list += self.afterevens(board, solution_list)
		solution_list += self.lowinverses(board)

	def claimevens(self, board):
		# Rule 1: Claimevens.
		for col in xrange(0, 7):
			for row in [1, 3, 5]:
				if board.open(row - 1, col):
					# This is a valid solution.
					# Figure out threats this solves.
					threats_solved = []
					for four in board.fours["X"]:
						if (row, col) in four:
							threats_solved.append(four)
					if len(threats_solved) > 0:
						solution_list.append(Solution("claimeven", [(row - 1, col), (row, col)], [], threats_solved))

	def baseinverses(self, board):
		# Rule 2: Baseinverses.
		for col in xrange(0, 7):
			# Find all pairs of directly playable squares.
			for col2 in xrange(col + 1, 7):
				if (board.can_play_in(col)) and (board.can_play_in(col2)):
					row = board.lowest_available(col)
					row2 = board.lowest_available(col2)
					threats_solved = []
					for four in board.fours["X"]:
						if (row, col) in four and (row2, col2) in four:
							threats_solved.append(four)
					if len(threats_solved) > 0:
						solution_list.append(Solution("baseinverse", [(row, col), (row2, col2)], [], threats_solved))
    
    def verticals(self, board):
		# Rule 3: Verticals.
		for col in xrange(0, 7):
			for row in [2, 4]:
				if board.open(row - 1, col):
					threats_solved = []
					for four in board.fours["X"]:
						if (row - 1, col) in four and (row, col) in four:
							threats_solved.append(four)
					if len(threats_solved) > 0:
						solution_list.append(Solution("vertical", [(row - 1, col), (row, col)], [], threats_solved))

	# Helper functions for afterevens.
	def claimeven_at(self, sq, solutions_list):
		# Hopefully this doesn't throw an index out of boudns error for non-claimevens.
		claimeven_sqs = [soln.squares[1] for soln in solutions_list if soln.rule == "claimeven"]
		return sq in claimeven_sqs

	def square_in_col_and_above(self, row, col, four):
		if len(four) == 0:
			return None
		else:
			(r, c) = four[0]
			if c == col and r >= row:
				return (r, c)
			else:
				return self.square_in_col_and_above(row, col, four[1:])

    def afterevens(self, board, solution_list):
		# Rule 4: Aftereven.
		# Find every group that can be completed by O by claimeven squares.
		aftereven_groups = []
		for own_four in board.fours["O"]:
			bad_squares = [sq for sq in own_four if board.open(*sq) and not self.claimeven_at(sq, solution_list)]
			if len(bad_squares) == 0:
				aftereven_groups.append(own_four)
		# For each aftereven group, add a Solution.
		for g in aftereven_groups:
			# Each aftereven group mitigates every threat with one open space in each aftereven column
			# above the aftereven square.
			open_squares = [sq for sq in g if board.open(*sq)]
			aftereven_cols = [col for (row, col) in open_squares]
			threats_solved = []
			for four in board.fours["X"]:
				works_for_each_column = True
				for (row, col) in open_squares:
					four_sq = self.square_in_col_and_above(row, col, four)
					if four_sq is None:
						works_for_each_column = False
				if works_for_each_column:
					threats_solved.append(four)
			solution_list.append(Solution("aftereven", [], aftereven_cols, threats_solved))

	def lowinverses(self, board):
		for col in range(0, 7):
			for col2 in range(col + 1, 7):
				for row in [2, 4]:
					for row2 in [2, 4]:
						if (board.open(col, row) and
							board.open(col, row-1) and
							board.open(col2, row2) and
							board.open(col2, row2 - 1)):
							threats_solved = []
							for four in board.fours["X"]:
								if ((col, row) in four and ((col2, row2) in four or (col, row-1) in four)):
									threats_solved.append(four)
								if ((col2, row2) in four and (col2, row2 - 1) in four):
									threats_solved.append(four)
							solution_list.append(
								Solution(
									"lowinverse",
									[(col, row), (col, row-1), (col2, row2), (col2, row2-1)],
									[col, col2],
									threats_solved
								)
							)




	def determine_solution_set(self, graph, chosen_sols):
		"""
		The purpose of this function is to take the graph of problems and
		solutions and return a set of compatible solutions which collectively
		solve every problem.
		"""
		problems = {k for k, v in graph if isinstance(k, Problem)}
		if problems == set():
			return chosen_sols
		else:
			# Determine the problem with the fewest solutions.
			most_difficult_problem = None
			for problem in problems:
				# If we cannot find a solution to a given problem, we have made
				# a mistake or the board is not in a drawable state for black.
				if len(graph[problem]) == 0:
					return None
				elif most_difficult_problem is None:
					most_difficult_problem = problem
				elif len(graph[problem]) > len(graph[most_difficult_problem]):
					most_difficult_problem = problem

			for soln in graph[most_difficult_problem]:
				new_graph = copy(graph)
				del new_graph[soln]
				# Deleting every neighbor of our chosen node solves two problems at once.
				# It removes from the graph every problem that this solution solves.
				# It also removes every solution incompatible with our chosen one.
				for nbr in graph[soln]:
					del new_graph[nbr]
				chosen = self.determine_solution_set(new_graph, chosen_sols.add(soln))
				if chosen is not None:
					return chosen
			return None

