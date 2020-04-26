import config

class Stock(dict):
    def remove(self, process):
        for key, input in process.input.items():
            # print("{}: {}: Removing {} {}".format(config.time, process.name, input, key))
            self[key] -= input
        # print("stock", self)

    def new(self, process):
        for key, output in process.output.items():
            # print("{}: {}: Creating {} {}".format(config.time, process.name, output, key))
            self[key] = self[key] + output if key in self else output
        # print("stock", self)
