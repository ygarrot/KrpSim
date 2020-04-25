from Process import *
from random import *
import numpy as np

def make_initial_population(processes):
    population = []
    for i in range(1000):
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
        doable = True
        if random() > chromosome[process_name]:
            #print("{} : {}".format(time, process_name))
            for key, input in current_process.input.items():
                #print("Removing {} {}".format(input, key))
                stock[key] -= input
            return True, True, stock
    return False, doable, stock

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
                process.busy, doable, stock = check_start_process(process, buf, stock, time, process_name, doable, chromosome)
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
    #print("lol")
    #print(list(parent1.values()))
    #print(list(parent1.values())[:crossover_point])
    #print(list(parent2.values()))
    #print(list(parent2.values())[crossover_point:])
    children_list = list(parent1.values())[:crossover_point]#.extend(list(parent2.values())[crossover_point:])
    children_list.extend(list(parent2.values())[crossover_point:])
    #print(children_list)
    children = {}
    i = 0
    for k in parent1:
        children[k] = children_list[i]
        i += 1
    #print(children)
    return children

def get_next_gen_population(population, score):
    new_population = []
    max_indices = np.argsort(score)[-667:]
    for i in max_indices:
        new_population.append(population[i])
    for i in range(333):
        new_population.append(get_crossover(new_population[i * 2], new_population[i * 2 + 1]))
    return new_population
#    score_threshold = sorted(score)[len(score)//2]
#    population_buffer = population
#    score_buffer = score
#    population_buffer = [population[i] for i, v in enumerate(score) if v >= score_threshold]
#    score_buffer = [score[i] for i, v in enumerate(score) if v >= score_threshold]
#    if len(population_buffer) % 2:
#        population_buffer.pop(score_buffer.index(min(score_buffer)))
#        score_buffer.pop(score_buffer.index(min(score_buffer)))
#    print(len(score_buffer))
#    print(len(population_buffer))
#    population_length = len(population_buffer)
#    i = 0
#    while i < population_length:
#        population_buffer.append(get_crossover(population_buffer[i], population_buffer[i + 1]))
#        i += 2
#    for i, chromosome in enumerate(population):
#        if score[i] < score_threshold:
#            population_buffer.pop(i)
#            score_buffer.pop(i)
#    print(sorted(score))
#    print(score_threshold)
#    new_population_buffer = []
#    if (len(score) > 50):
#        max_indices = np.argsort(score)[-67:]
#        for i in max_indices:
#            new_population_buffer.append(population_buffer[i])
#    else:
#        new_population_buffer = population_buffer
#    return new_population_buffer

def krpsim(stock, processes, optimize):
    population = make_initial_population(processes)
    for generation in range(1000):
        score = []
        for i, chromosome in enumerate(population):
            #print(i)
            stock_buffer, time_buffer = run_processes(processes, stock.copy(), chromosome)
            score.append(get_score(stock_buffer, time_buffer, optimize))
        population = get_next_gen_population(population, score)
        print(sorted(score))
        print(np.mean(score))
