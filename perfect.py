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
	def __init__(self, rule, squares, threats):
		self.rule = rule
		self.squares = squares
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
					if (not board.cannot_play_in(i)):
						c.play(i)
						for j in xrange(0, 7):
							if (not board.cannot_play_in(j)):
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

