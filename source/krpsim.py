from Process import *
from random import *
import numpy as np

def make_initial_population(processes):
    population = []
    for i in range(100):
        chromosome = {}
        for process in processes:
            chromosome[process] = random()
        population.append(chromosome)
    return population

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

def check_start_process(current_process, buf, stock, time, process_name, doable, chromosome):
    """
    Check if buf contains all process' inputs
    if so remove from the stock the input and start the process setting it to
    busy.
    """
    if all (current_input in buf for current_input in current_process.input.keys()):
#        chromosome[process_name] = chromosome[process_name] - 0.001 if chromosome[process_name] - 0.001 > 0.1 else 0.1
        doable = True
        if random() < chromosome[process_name]:
            #print("{} : {}".format(time, process_name))
            for key, input in current_process.input.items():
                #print("Removing {} {}".format(input, key))
                stock[key] -= input
            return True, True, stock, chromosome
#    else:
#        chromosome[process_name] = chromosome[process_name] + 0.001 if chromosome[process_name] + 0.001 < 0.9 else 0.9
    return False, doable, stock, chromosome

def check_end_process(process, stock, process_name):
    """
    Check if process ended
    if so, adding it's output to the stock and setting busy to false.
    """
    process.delta_time += 1
    if (process.delta_time is process.time):
        for key, output in process.output.items():
            #print("Creating {} {}".format(output, key))
            process.requested -= output
            stock[key] = stock[key] + output if key in stock else output
        process.delta_time = 0
        process.busy       = False
        #print("Process {} ended".format(process_name))
    return process, stock

def run_processes(processes, stock, chromosome):
    buf = {}
    time = 0
    doable = True
    while time < 3000:
        doable = False
        for process_name, process in processes.items():
            if not process.busy:
                buf = check_stock_for_process(process, stock)
                process.busy, doable, stock, chromosome = check_start_process(process, buf, stock, time, process_name, doable, chromosome)
            else:
                doable = True
                process, stock = check_end_process(process, stock, process_name)
        if not doable:
            #print("no more process doable at time {}".format(time))
            break
        time += 1
    return stock, time

def get_score(stock, time, optimize):
    score = 0
    if "time" in optimize:
        score -= time
    for k in stock:
        if k in optimize:
            score += stock[k]
    return score

def get_crossover(parent1, parent2):
    crossover_point = int(random() * len(parent1))
    children_list = list(parent1.values())[:crossover_point]
    children_list.extend(list(parent2.values())[crossover_point:])
    children = {}
    i = 0
    for k in parent1:
        children[k] = children_list[i]
        i += 1
    return children

def get_next_gen_population(population, score):
    new_population = []
    max_indices = np.argsort(score)[-67:]
    for i in max_indices:
        new_population.append(population[i])
    for i in range(33):
        new_population.append(get_crossover(new_population[i * 2], new_population[i * 2 + 1]))
    return new_population

def krpsim(stock, processes, optimize):
    population = make_initial_population(processes)
    for generation in range(1000):
        score = []
        for i, chromosome in enumerate(population):
            #print(i)
            stock_buffer, time_buffer = run_processes(processes, stock.copy(), chromosome)
            score.append(get_score(stock_buffer, time_buffer, optimize))
            if len(score) - 1 == score.index(max(score)):
                fittest_stock = stock_buffer
        population = get_next_gen_population(population, score)
        print("Fittest population")
        print(population[score.index(max(score))])
        print("Fittest stock")
        print(fittest_stock)
        print("Sorted scores")
        print(sorted(score))
        print("Mean score")
        print(np.mean(score))
