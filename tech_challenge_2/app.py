import sys
import os
import random

# Add the parent directory to the path so we can import the coins module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# To cripto the good sharpe ratio is 1.5, to stock is 1, to forex is 0.5
good_sharpe_ratio = 1.5

population_size = 20

coint_qtd = 5

from ag import (
    generate_population,
    calculate_fitness,
    calculate_sharpe_ratio_for_multiple_cryptos,
    verify_finishing_condition,
    selection_elitism,
    selection_tournament,
    crossover,
    mutate,
)

wallet = []

# Test fitness
def main55():
    population = [
        {
            'coins': [ 'Bitcoin', 'BNB'],
            'weights': [0.5, 0.5]
        },
    ]
    fitness = calculate_fitness(population)
    print(fitness)

def main22():
    # Exemplo de uso
    paths = [ 'Bitcoin', 'BNB']  # Substitua com os caminhos para seus arquivos
    weights = [0.5, 0.5]  # Pesos correspondentes para as criptomoedas

    sharpe_ratio, retorno_anualizado, volatilidade_anualizada = calculate_sharpe_ratio_for_multiple_cryptos(paths, weights)

    print(f'Índice de Sharpe: {sharpe_ratio:.2f}')
    print(f'Retorno Anualizado: {retorno_anualizado:.2%}')
    print(f'Volatilidade Anualizada: {volatilidade_anualizada:.2%}')

def main():
    running = True
    has_elitism = False
    has_elitism_and_tornament = True
    numGeneration = 1

    ## generates population of ten wallets with 6 coins each
    population = generate_population(
        coins_quantity=coint_qtd, population_size=population_size
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
        if has_elitism_and_tornament:
            selected = selection_elitism(population_with_fitness)[:1] + selection_tournament(population_with_fitness)[:1]
        elif has_elitism:
            selected = selection_elitism(population_with_fitness)
        else:
            selected = selection_tournament(population_with_fitness)

        print(f"Best wallet fitness: {selected[0].get('fitness')}")
        print(f"Best wallet weight: {selected[0].get('coins')}")
        print(f"Best wallet weight: {selected[0].get('weights')}")
        print(f"Best wallet fitness: {selected[1].get('fitness')}")
        print(f"Best wallet coins: {selected[1].get('coins')}")
        print(f"Best wallet weights: {selected[1].get('weights')}")

        new_individual = crossover(random.choices(selected, k=1)[0], random.choices(selected, k=1)[0])
        mutated_individual = mutate(new_individual)

        # start a new population
        new_population = [mutated_individual]
        # ensure i don't lose the best wallet
        new_population.extend(selected)

        # Generate new random individuals to fill 50% of the population
        num_random_individuals = population_size // 2
        new_random_individuals = generate_population(coins_quantity=coint_qtd, population_size=num_random_individuals)

        # Insert new random individuals one by one into new_population
        for individual in new_random_individuals:
            new_population.append(individual)
        
        while len(new_population) < population_size:
            print(f"ENTROU AQUI population {len(new_population)} population size {population_size}")
            parent1, parent2 = random.choices(population[:population_size], k=2)
            child = crossover(parent1, parent2)
            child = mutate(child)

            child2 = crossover(parent1, child)
            child2 = mutate(child2)

            child3 = crossover(child, parent2)
            child3 = mutate(child3)

            new_population.extend([child])
            new_population.extend([child2])
            new_population.extend([child3])

        # overrides the population
        population.clear()
        population = new_population
        # print(population)
        print("-------------------------------------------------")
        numGeneration += 1
