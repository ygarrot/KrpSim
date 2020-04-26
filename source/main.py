#!/usr/bin/env python3
from config import processes, optimize, stock
from parser import parse
import sys
from krpsim import *

def main():
    optimize = parse(sys.argv[1])
    krpsim(stock, processes, optimize)


if __name__ == '__main__':
    main()

