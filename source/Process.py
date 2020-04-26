import config
class Process:
    """
    t : time needed to complete
    dt : progress towards completion
    """
    def __init__(self, input = {}, output={}, time = 0):
        self.input      = input
        self.output     = output
        self.time       = time
        self.delta_time = 0
        self.busy       = False
        self.doable     = False
        self.requested  = 0
        self.name       = ""

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

    def is_doable(self, buf):
        self.doable = all (current_input in buf for current_input in self.input.keys())
        return self.doable

    def start(self):
        # print("{}: {}".format(config.time, self.name))
        self.busy   = True

    def update(self, time):
        self.delta_time += time

    def done(self):
        return self.delta_time >= self.time

    def end(self):
        # print("Process {} ended".format(self.name))
        self.delta_time = 0
        self.busy       = False

