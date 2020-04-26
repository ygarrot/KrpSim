#!/usr/bin/env python3
from config import processes, optimize, stock, possible_stock, opt_len
from parser import parse
import sys
from krpsim import *

def main():
    optimize = parse(sys.argv[1])
    print("Nice file ! {} processes, {} stocks, {} to optimize".format(len(processes), len(possible_stock), config.opt_len))
    krpsim(stock, processes, optimize)


if __name__ == '__main__':
    main()

