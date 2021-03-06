#!/usr/bin/env python3

from Process import *
import re
from lark import Lark, Transformer, v_args, Tree, UnexpectedInput
import argparse
import traceback
import logging
import copy
from config import *

try:
    input = raw_input   # For Python2 compatibility
except NameError:
    pass

calc_grammar = r"""
    ?start: (initial_resources _LI)+ rules _LI (rules _LI|_LI)+

    ?initial_resources: elem    -> initial_resources
    ?elem:  MWORD ":" NUMBER    -> elem
    ?liste: elem ";" | elem
    ?output: "(" liste+ "):" | ":"
    ?input:  "(" liste+ "):" | ":"
    ?rules:  MWORD ":" input output NUMBER -> set_rules

    ?goal: MWORD| MWORD ";"
    ?optimize: "optimize:(" goal+  ")" ->set_goal

    _LI: (_COMMENT | LF+)
    _COMMENT: /#.*\n/
    MWORD: /([a-zA-Z0-9_])/+

    NUMBER: SIGNED_NUMBER
    %import common.UCASE_LETTER
    %import common.SIGNED_NUMBER
    %import common.WORD
    %import common.LF
    %ignore _COMMENT
"""

class trans(Transformer):
    def initial_resources(self, args):
        if args:
            stock[str(args[0][0])] = int(args[0][1])

    def elem(self, args):
        return (str(args[0]), int(args[1]))

    def output(self, args):
        return  args

    def input(self, args):
        return  args

    def set_rules(self, args):
        process = Process()
        process.time = int(args[3])

        if (isinstance(args[1], list)):
            process.input = {key:value for (key, value) in args[1]}
        else:
            process.input = {args[1][0]: args[1][1]}

        if args[2]:
            if (isinstance(args[2], list)):
                process.output = {key:value for (key, value) in args[2]}
            else:
                process.output = {args[2][0]: args[2][1]}

        if args[2] and str(args[2][0]) not in config.possible_stock:
            config.possible_stock.append(str(args[2][0]))
        if str(args[1][0]) not in config.possible_stock:
            config.possible_stock.append(str(args[1][0]))
        process.name = str(args[0])
        processes[str(args[0])] = process
        # print(str(args[0]), process)

def parse(name_file):
    calc_parser = Lark(calc_grammar, parser='lalr', debug=True, transformer=trans())
    with open(name_file, 'r') as myfile:
        file_content=myfile.read()
    opt = re.search('optimize:\((.*)\)', re.sub('#.*', '', file_content), re.IGNORECASE)
    if not opt:
        exit("nothing to optimize")
    config.optimize = opt.group(1).split(';')
    config.opt_len = len(config.optimize) - 1 if 'time' in config.optimize else len(config.optimize)
    file_content = re.sub('optimize:(.*)', '', file_content)

    try:
        tree = calc_parser.parse(file_content)
    except UnexpectedInput as e:
        print(e)
    return (config.optimize)
