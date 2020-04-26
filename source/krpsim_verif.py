#!/usr/bin/env python3

from Process import *
from config import processes, optimize, stock, possible_stock
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
    ?new_process:  NUMBER ":" MWORD         -> new_process
    ?time: "no more process doable at time " NUMBER -> end_of_production
    ?stock: "Stock :"
    ?stock_summary_end: MWORD "=>" NUMBER -> summary_end

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
        #TODO
        # for arg in args:
        #     print(arg)
    def new_process(self, args):
        global process_history
        if len(args) is not 2:
            exit("Production of a new process must have a time and the process name")
        time, process_name = args
        if process_name not in processes:
            exit("Process doesn't exist")
        try:
            process_history.append((int(time), str(process_name)))
        except:
            exit("Must be int and str")

    def summary_end(self, args):
        global stock_summary
        if len(args) is not 2:
            exit("Summary must have a stock_name and the number of stock")
        stock_name, stock_value = args
        try:
            stock_summary.append((str(stock_name), int(stock_value)))
        except:
            exit("Must be str and int")

    def end_of_production(self, args):
        if len(args) is not 1:
            exit("end of production must be a unique int")
        global end_of_production
        try:
            end_of_production = int(args[0])
        except:
            exit("Must be int")




def check_process_history(buf, args):
    time, process_name = args
    for process in processes.values():
        if process.busy:
            process, buf = update_process(process, buf, int(time))
    process = processes[process_name]
    if not process.is_doable(buf):
        exit("not enough ressources in stock to produce this process")
    process.start()
    buf.remove(process)
    return buf

def check_end_of_process_history(buf):
    time = end_of_production
    for process in processes.values():
        if process.busy:
            process, buf = update_process(process, buf, time)
    return buf
    print("buf, ", buf)

def check_stock_summary(buf, args):
    stock_name, stock_value = args
    if stock_name not in buf:
        if stock_name not in config.possible_stock \
            or stock_value is not 0:
            exit("stock_name not in stock")
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

if __name__ == '__main__':
    main()

