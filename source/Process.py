class Process:
    """
    i : input
    o : output
    t : time needed to complete
    dt : progress towards completion
    b : busy or not
    r : requested or not
    """
    def __init__(self, input = {}, output={}, time = 0):
        self.i = input
        self.o = output
        self.t = time
        self.dt = 0
        self.b = False
        self.r = 0

    def __str__(self):
        return ("time: {}\n"
                "busy: {}\n"
                "requested: {}\n"
                "progreess: {}\n"
                "input: {}\n"
                "output: {}\n"
                ).format(
                  self.t,
                  self.b,
                  self.r,
                  self.dt,
                  self.i.items(),
                  self.o.items())
