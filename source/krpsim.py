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

def check_start_process(process, buf, stock, chromosome):
    """
    Check if buf contains all process' inputs
    if so remove from the stock the input and start the process setting it to
    busy.
    """
    if process.is_doable(buf):
#        chromosome[process.name] = chromosome[process.name] - 0.001 if chromosome[process.name] - 0.001 > 0.1 else 0.1
        if random() < chromosome[process.name]:
            process.start()
            stock.remove(process)
#    else:
#        chromosome[process.name] = chromosome[process.name] + 0.001 if chromosome[process.name] + 0.001 < 0.9 else 0.9
    return process, stock, chromosome

def update_process(process, stock, time=1):
    """
    Check if process ended
    if so, adding it's output to the stock and setting busy to false.
    """
    process.update(time)
    if (process.done()):
        stock.new(process)
        process.end()
    return process, stock

def run_processes(processes, stock, chromosome):
    buf = {}
    time = 0
    doable = False
    while time < 3000:
        for process in processes.values():
            if not process.busy:
                buf = check_stock_for_process(process, stock)
                process, stock, chromosome = check_start_process(process, buf, stock, chromosome)
            else:
                process, stock = update_process(process, stock)
        doable = False
        for process in processes.values():
            if (process.busy or process.doable):
                doable = True
        if not doable:
            # print("no more process doable at time {}".format(time))
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
#     score += sum([stock[process] for process in stock if process in optimize])
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
    print("max_indices:", max_indices)
    for i in max_indices:
        new_population.append(population[i])
    for i in range(33):
        new_population.append(get_crossover(new_population[i * 2], new_population[i * 2 + 1]))
    return new_population

import copy
def krpsim(stock, processes, optimize):
    population = make_initial_population(processes)
    for generation in range(1000):
        score = []
        for i, chromosome in enumerate(population):
            stock_buffer, time_buffer = run_processes(processes, copy.deepcopy(stock), chromosome)
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
