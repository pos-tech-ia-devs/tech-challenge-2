import sys
import os
import random

# Add the parent directory to the path so we can import the coins module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# To cripto the good sharpe ratio is 1.5, to stock is 1, to forex is 0.5
good_sharpe_ratio = 1.5

population_size = 20

from ag import (
    generate_population,
    calculate_fitness,
    verify_finishing_condition,
    selection_elitism,
    selection_tournament,
    crossover,
    mutate,
)

wallet = []


def main():
    running = True
    has_elitism = False
    numGeneration = 1

    ## generates population of ten wallets with 6 coins each
    population = generate_population(
        coins_quantity=6, population_size=population_size
    )
    # print(population)
    while running:
        print(f"Generation: {numGeneration}")
        print("-------------------------------------------------")
        ## calculates the fitness of each wallet
        population_with_fitness = calculate_fitness(population)

        ## check if the finishing condition is met
        can_stop = verify_finishing_condition(population_with_fitness, good_sharpe_ratio)

        ## if the finishing condition is met, print the best wallet and stop the loop
        if can_stop:
            print(f"Best wallet: {population_with_fitness}")
            running = False
            break


        ## selection of the best wallets
        selected = []
        if has_elitism:
            selected = selection_elitism(population_with_fitness)
        else:
           selected = selection_tournament(population_with_fitness)

        print(f"Best wallet this now: {selected}")
        new_individual = crossover(random.choices(selected, k=1)[0], random.choices(selected, k=1)[0])
        mutated_individual = mutate(new_individual)

        # start a new population
        new_population = [mutated_individual]
        # ensure i don't lose the best wallet
        new_population.extend(selected)
        # print(f"new population: {new_population}")
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population[:population_size], k=2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.extend([child])

        # overrides the population
        population.clear()
        population = new_population
        # print(population)
        print("-------------------------------------------------")
        numGeneration += 1