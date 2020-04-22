#!/usr/bin/env python3
from config import processes, optimize, stock
from parser import parse
import sys

def main():
    parse(sys.argv[1])
    for i in processes:
        print(processes[i])


if __name__ == '__main__':
    main()

