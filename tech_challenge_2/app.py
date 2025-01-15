import sys
import os
import random
import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from ag import (
    generate_population,
    calculate_fitness,
    verify_finishing_condition,
    selection_elitism,
    selection_tournament,
    crossover,
    mutate,
)


def format_portfolio(assets, weights):
    """
    Formats a list of assets and their weights into a user-friendly string.

    Args:
        assets (list): List of asset names.
        weights (list): List of weights corresponding to the assets.

    Returns:
        str: A formatted string with the assets and their weights as percentages.
    """
    if len(assets) != len(weights):
        raise ValueError("As listas de ativos e pesos devem ter o mesmo comprimento.")

    formatted = [
        f"{asset}: {weight * 100:.0f}%" for asset, weight in zip(assets, weights)
    ]
    return ", ".join(formatted)


def run_app(
    good_sharpe_ratio,
    risk_free_rate,
    population_size,
    coins_qtd,
    max_generations,
    has_elitism_and_tournament="elitism_and_tournament",
    debug=False,
):
    running = True
    numGeneration = 1
    best_wallet = None

    population = generate_population(
        coins_quantity=coins_qtd, population_size=population_size
    )

    if debug == False:
        st.markdown(
            """
            ---
            """
        )

        log_txt_box = st.empty()
        log_txt = ""

    while running:
        ## calculates the fitness of each wallet
        population_with_fitness = calculate_fitness(population, risk_free_rate)

        ## check if the finishing condition is met
        can_stop = verify_finishing_condition(
            population_with_fitness, good_sharpe_ratio
        )

        ## if the finishing condition is met, print the best wallet and stop the loop
        if can_stop or numGeneration == max_generations:
            if debug:
                print("-------------------------------------------------")
                print(f"Best wallet: {best_wallet}")
            else:

                log_txt_box.empty()

                with st.container():
                    st.subheader("🔍 Resultado Final")
                    st.markdown(
                        f"📈 **Melhor Índice de Sharpe encontrado:** `{best_wallet.get('fitness').round(2)}`",
                        help="O Índice de Sharpe é uma métrica que avalia a relação entre retorno e risco de uma carteira de investimentos.",
                    )

                    result = format_portfolio(
                        best_wallet.get("coins"), best_wallet.get("weights")
                    )

                    with st.container():
                        st.write("💡 **Melhor Configuração de Carteira:**")
                        st.markdown(result, unsafe_allow_html=True)

                    st.info(
                        "🔔 Dica: Uma carteira bem balanceada considera tanto o retorno esperado quanto o risco associado. "
                        "Certifique-se de revisar os dados antes de investir.",
                        icon="💼",
                    )

                running = False
                break

        ## selection of the best wallets
        selected = []
        if has_elitism_and_tournament == "elitism_and_tournament":
            selected = (
                selection_elitism(population_with_fitness)[:1]
                + selection_tournament(population_with_fitness)[:1]
            )
        elif has_elitism_and_tournament == "elitism":
            selected = selection_elitism(population_with_fitness)
        else:
            selected = selection_tournament(population_with_fitness)

        best_wallet = selected[0]

        if debug:
            print(f"Best wallet fitness: {selected[0].get('fitness').round(2)}")
            print(f"Best wallet coins: {selected[0].get('coins')}")
            print(f"Best wallet weights: {selected[0].get('weights')}")
            print("\n")
            print(f"Actual wallet fitness: {selected[1].get('fitness').round(2)}")
            print(f"Actual wallet coins: {selected[1].get('coins')}")
            print(f"Actual wallet weights: {selected[1].get('weights')}")
        else:
            log_txt = (
                f"📊 Progresso da Geração: **{numGeneration}/{max_generations}**\n\n"
            )

            log_txt += f"📈 Melhor Índice de Sharpe Atual: **{selected[0].get('fitness').round(2)}**\n\n"

            wallet_formatted = format_portfolio(
                selected[0].get("coins"), selected[0].get("weights")
            )

            log_txt += f"💼 Melhor Carteira e Alocação Atual:\n**{wallet_formatted.upper()}**\n\n"

            log_txt_box.markdown(log_txt)

        new_individual = crossover(
            random.choices(selected, k=1)[0], random.choices(selected, k=1)[0]
        )
        mutated_individual = mutate(new_individual)

        # start a new population
        new_population = [mutated_individual]
        # ensure i don't lose the best wallet
        new_population.extend(selected)

        # Generate new random individuals to fill 50% of the population
        num_random_individuals = population_size // 2
        new_random_individuals = generate_population(
            coins_quantity=coins_qtd, population_size=num_random_individuals
        )

        # Insert new random individuals one by one into new_population
        for individual in new_random_individuals:
            new_population.append(individual)

        while len(new_population) < population_size:
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
        numGeneration += 1


def main():
    run_app(
        good_sharpe_ratio=1.5,
        risk_free_rate=0.04,
        population_size=20,
        coins_qtd=5,
        max_generations=100,
        debug=True,
    )
