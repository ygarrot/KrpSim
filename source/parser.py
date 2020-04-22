#!/usr/bin/env python3

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
    ?start: (initial_resources _LI)+ (rules _LI)+ _LI+ optimize _LI

    ?initial_resources: elem
    ?elem:  MWORD ":" NUMBER    -> elem
    ?liste: elem ";" elem | elem
    ?rules: MWORD ":(" liste "):(" liste "):" NUMBER -> set_rules

    ?optimize: "optimize:(" MWORD  ")" -> set_goal

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

calc_parser = Lark(calc_grammar, parser='lalr',
        debug=True)

with open(sys.argv[1], 'r') as myfile:
    file_content=myfile.read()
# file_content = re.sub('#.*', '', file_content).strip()
try:
    tree = calc_parser.parse(file_content)
except UnexpectedInput as e:
    print(e)
