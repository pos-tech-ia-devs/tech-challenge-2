import sys
import os

# Add the parent directory to the path so we can import the coins module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ag import (
    generate_population,
    calculate_fitness,
    verify_finishing_condition,
    selection,
    crossover,
    mutate,
)

wallet = []


def main():
    result = crossover(
        {
            "coins": ["Bitcoin", "Ethereum", "BNB"],
            "weights": [
                0.4,
                0.3,
                0.3,
            ],
            "fitness": 1.5,
        },
        {
            "coins": ["Solana", "Bitcoin", "Pepe"],
            "weights": [
                0.5,
                0.25,
                0.25,
            ],
            "fitness": 1.5,
        },
    )
    mutate_result = mutate(result)

    print(mutate_result)
