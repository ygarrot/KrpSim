from Process import *

def get_requests(processes, s, main_requests, sub_requests, current_process):
    requested = current_process.requested
    for j in range(10):
        for process in processes.values():
            if any (output in main_requests for output in process.output.keys())\
                    or any (output in sub_requests.keys() for output in process.output.keys()):
                for key, input in process.input.items():
                    sub_requests[key] = input
    if requested <= 0:
    #if all (p[k].r <= 0 for k in p):
        requested += sum([request for key, request in sub_requests.items() if key in current_process.output])
        requested += sum([1       for key          in main_requests        if key in current_process.output])
    return requested, sub_requests;

def check_stock_for_process(current_process, stock):
    """
    Parcours les inputs d'un process
    Stock dans un buf les inputs qui sont dans le stock
    en quantite suffisante.
    Retourne le buf
    """
    buf = {}
    for key, value in current_process.input.items():
        if key in stock and stock[key] >= value:
            buf[key] = True
    return buf

def check_start_process(current_process, buf, stock, time, i, doable):
    """
    Check if buf contains all process' inputs
    if so remove from the stock the input and start the process setting it to
    busy.
    """
    if all (current_input in buf for current_input in current_process.input.keys()):
        print("{} : {}".format(time, i))
        for key, input in current_process.input.items():
            print("Removing {} {}".format(input, key))
            stock[key] -= input
        return True, True, stock
    return False, doable, stock

def check_end_process(current_process, stock, key):
    """
    Check if process ended
    if so, adding it's output to the stock and setting busy to false.
    """
    current_process.delta_time += 1
    if (current_process.delta_time is current_process.time):
        for key, output in current_process.output.items():
            print("Creating {} {}".format(output, key))
            current_process.requested -= output
            stock[key] = stock[key] + output if key in stock else output
        current_process.delta_time = 0
        current_process.busy       = False
        print("Process {} ended".format(key))
    return current_process, stock

def krpsim(stock, processes, optimize):
    main_requests = [elem for elem in optimize if elem != "time"]
    buf           = {}
    sub_requests  = {}
    time          = 0

    while time < 10000:
        doable = False
        for i, process in processes.items():
            buf                             = {}
            process.requested, sub_requests = get_requests(processes, stock, main_requests, sub_requests, process)

            if not process.busy and process.requested > 0:
                buf = check_stock_for_process(process, stock)
                process.busy, doable, stock = check_start_process(process, buf, stock, time, i, doable)
            elif process.busy:
                doable = True
                processes[i], stock = check_end_process(process, stock, i)

        if not doable:
            print("no more process doable at time {}".format(time))
            break
        time += 1
    print(stock)
    print(time)
