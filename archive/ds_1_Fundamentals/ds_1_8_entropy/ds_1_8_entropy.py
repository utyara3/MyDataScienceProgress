import math
import collections
from pprint import pprint


def calculate_entropy(data: list[str]) -> float:
    """
    Вычисление энтропии для списка меток.
    """
    counter = collections.Counter(data)
    total_count = len(data)

    entropy = 0.0
    for count in counter.values():
        "H(X) = - Σ (pᵢ * log₂(pᵢ))"
        possibility = count/total_count
        entropy -= possibility * math.log2(possibility)

    return entropy

# demonstration

if __name__ == "__main__":
    basket1 = ["apple"] * 10
    basket2 = ["apple"] * 5 + ["orange"] * 5
    basket3 = ["apple"] * 3 + ["banana"] * 3 + ["orange"] * 3 + ["tomato"]

    entropy1 = round(calculate_entropy(basket1), 3)
    entropy2 = round(calculate_entropy(basket2), 3)
    entropy3 = round(calculate_entropy(basket3), 3)

    pprint(f"Basket1: {basket1}, entropy = {entropy1}")
    pprint(f"Basket2: {basket2}, entropy = {entropy2}")
    pprint(f"Basket3: {basket3}, entropy = {entropy3}")
    
