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
        self.input      = input
        self.output     = output
        self.time       = time
        self.delta_time = 0
        self.busy       = False
        self.requested  = 0

    def __str__(self):
        return ("time: {}\n"
                "busy: {}\n"
                "requested: {}\n"
                "progress: {}\n"
                "input: {}\n"
                "output: {}\n"
                ).format(
                  self.time,
                  self.busy,
                  self.requested,
                  self.delta_time,
                  self.input.items(),
                  self.output.items())
