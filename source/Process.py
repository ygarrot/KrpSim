class Process:
	"""
	i : input
	o : output
	t : time needed to complete
	dt : progress towards completion
	b : busy or not
	r : requested or not
	"""
	def __init__(self, input, output, time):
		self.i = input
		self.o = output
		self.t = time
		self.dt = 0
		self.b = False
		self.r = 0
