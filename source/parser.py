#!/usr/bin/env python3

from Process import *
import re
from lark import Lark, Transformer, v_args, Tree, UnexpectedInput
import argparse
import traceback
import logging
import sys
# from config import *

try:
    input = raw_input   # For Python2 compatibility
except NameError:
    pass

calc_grammar = r"""
    ?start: (initial_resources _LI)+ rules _LI (rules _LI|_LI)+

    ?initial_resources: elem    -> initial_resources
    ?elem:  MWORD ":" NUMBER    -> elem
    ?liste: elem ";" | elem

    ?output: "):(" liste+ "):" | "):"
    ?input:  ":(" liste+
    ?rules:  MWORD input output NUMBER -> set_rules

    ?goal: MWORD| MWORD ";"
    ?optimize: "optimize:(" goal+  ")" ->set_goal

    _LI: (_COMMENT | LF+)
    _COMMENT: /#.*\n/
    MWORD: /([a-zA-Z0-9_])/+

    %import common.UCASE_LETTER
    %import common.NUMBER
    %import common.WORD
    %import common.WS_INLINE
    %import common.LF
    %ignore WS_INLINE
    %ignore _COMMENT
"""

stock = {}
processes = {}
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
        process.t = args[3]
        if (isinstance(args[1], list)):
            process.i = {key:value for (key, value) in args[1]}
        else:
            process.i[args[1][0]] = args[1][1]
        if (isinstance(args[2], list)):
            process.o = {key:value for (key, value) in args[2]}
        else:
            process.o[args[2][0]] = args[2][1]
        processes[args[0]] =process




calc_parser = Lark(calc_grammar, parser='lalr', debug=True, transformer=trans())


with open(sys.argv[1], 'r') as myfile:
    file_content=myfile.read()
opt = re.search('optimize:\((.*)\)', re.sub('#.*', '', file_content), re.IGNORECASE)
if not opt:
    exit()
toto = opt.group(1).split(';')
print(toto)

file_content = re.sub('optimize:(.*)', '', file_content)

try:
    tree = calc_parser.parse(file_content)
except UnexpectedInput as e:
    print(e)

for i in processes:
	print(i)
	print(processes[i].i.items())
	print(processes[i].o.items())
	print(str(processes[i].t))
