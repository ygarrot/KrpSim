#!/usr/bin/env python3

from Process import *
import config
from lark import Lark, Transformer, v_args, Tree, UnexpectedInput
from parser import parse
from krpsim import update_process
import sys

buf = {}
process_history = []
stock_summary = []
end_of_production = 0

calc_grammar = r"""
    ?start: stock_summary_begin new_process+ time stock stock_summary_end+

    ?stock_summary_begin: "Nice file ! " NUMBER "processes, " NUMBER "stocks, " NUMBER "to optimize" _LI -> summary_begin
    ?new_process:  NUMBER ":" MWORD                 -> new_process
    ?time: "no more process doable at time " NUMBER -> end_of_production
    ?stock: "Stock :"
    ?stock_summary_end: MWORD "=>" NUMBER           -> summary_end

    _LI: (_COMMENT | LF+)
    _COMMENT: /#.*\n/
    MWORD: /([a-zA-Z0-9_])/+

    NUMBER: SIGNED_NUMBER
    %import common.UCASE_LETTER
    %import common.SIGNED_NUMBER
    %import common.WORD
    %import common.LF
    %import common.WS
    %ignore _COMMENT
    %ignore WS
"""

def parse_verif(name_file):
    calc_parser = Lark(calc_grammar, parser='lalr', debug=True, transformer=trans())
    with open(name_file, 'r') as myfile:
        file_content=myfile.read()
    try:
        tree = calc_parser.parse(file_content)
    except UnexpectedInput as e:
        print(e)

class trans(Transformer):
    def summary_begin(self, args):
        if len(args) is not 3:
            exit("summary must have 3 differentes values")
        processes, stock, optimize = args
        if int(processes) != len(config.processes)\
                or int(stock) != len(config.possible_stock)\
                or int(optimize) != config.opt_len:
            exit("Bad summary")
    def new_process(self, args):
        global process_history
        time, process_name = args
        if process_name not in config.processes:
            exit("Process doesn't exist")
        process_history.append((int(time), str(process_name)))

    def summary_end(self, args):
        global stock_summary
        stock_summary.append((str(args[0]), int(args[1])))

    def end_of_production(self, args):
        global end_of_production
        end_of_production = int(args[0])

def check_process_history(buf, args):
    time, process_name = args
    for process in config.processes.values():
        if process.busy:
            process, buf = update_process(process, buf, int(time))

    process = config.processes[process_name]
    if not process.is_doable(buf):
        exit("not enough ressources in stock to produce this process")
    process.start()
    buf.remove(process)
    return buf

def check_end_of_process_history(buf):
    time = end_of_production
    for process in config.processes.values():
        if process.busy:
            process, buf = update_process(process, buf, time)
    return buf

def check_stock_summary(buf, args):
    stock_name, stock_value = args
    if stock_name not in buf:
        if stock_name not in config.possible_stock \
            or stock_value is not 0:
            exit("{} not in stock".format(stock_name))
    if buf[stock_name] is not stock_value:
        exit("invalid stock value for stock_name")

def main():
    global buf
    global process_history

    if len(sys.argv) is not 3:
        exit("Give me 2 file")

    optimize = parse(sys.argv[1])
    buf = config.stock
    parse_verif(sys.argv[2])

    for creation in process_history:
        buf = check_process_history(buf, creation)

    buf = check_end_of_process_history(buf)

    for stock in stock_summary:
        check_stock_summary(buf, stock)
    print("File is correct")

if __name__ == '__main__':
    main()

