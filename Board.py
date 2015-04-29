from copy import copy, deepcopy

class Board(object):
	"""docstring for Board"""
	def __init__(self):
		super(Board, self).__init__()
		self.reset()

	def reset(self):
		b = ['.','.','.','.','.','.']
		self.cols = [copy(b),copy(b),copy(b),copy(b),copy(b),copy(b),copy(b)]
		self.current_player = "X"
		
	def at(self, row, col):
		self.cols[col][row]

	def cannot_play_in(self, col):
		not ('_' in self.cols[col])

	def switch_player(self):
		if self.current_player == "X":
			self.current_player = "O"
		else:
			self.current_player = "X"

	def lowest_available(self, col):
		col -= 1
		for i, sq in enumerate(self.cols[col]):
			if sq == '.':
				return i
		return ValueError("Column full")

	# 1-indexed cols
	def play(self, col):
		assert 0 < col < 8
		self.cols[col - 1][self.lowest_available(col)] = self.current_player
		self.switch_player()

	# This probably shouldn't be a method.
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

if __name__ == "__main__":
	b = Board()
	while(True):
		play = input("Where to play?: ")
		b.play(play)
		b.display_board()