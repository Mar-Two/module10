from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable:
    count = 0

    def incremente() -> int:
        nonlocal count
        count += 1
        return count
    return incremente


def spell_accumulator(initial_power: int) -> Callable:
    if not isinstance(initial_power, int):
        raise ValueError("Error: initial_power must be an int")

    def accumulator(amount: int) -> int:
        if not isinstance(amount, int):
            raise ValueError("Error: amount must be an accumulate int")
        nonlocal initial_power
        initial_power += amount
        return initial_power
    return accumulator


def enchantment_factory(enchantment_type: str) -> Callable:
    if not isinstance(enchantment_type, str):
        raise ValueError("Error: enchantment_type must be a str")
    return lambda item_name: f"{enchantment_type} {item_name}"


def memory_vault() -> dict[str, Callable]:
    my_dict = {}

    def store(key: Any, value: Any) -> None:
        my_dict[key] = value

    def recall(key) -> Any:
        return my_dict.get(key, "Memory not found")
    return {'store': store, 'recall': recall}


if __name__ == '__main__':
    try:
        print("Testing mage counter...")
        counter_a = mage_counter()
        counter_b = mage_counter()
        print(f"counter_a call 1: {counter_a()}")
        print(f"counter_a call 2: {counter_a()}")
        print(f"counter_b call 1: {counter_b()}")
    except Exception as e:
        print(e)

    try:
        print("\nTesting spell accumulator...")
        acc = spell_accumulator(100)
        print(f"Base 100, add 20: {acc(20)}")
        print(f"Base 100, add 30: {acc(30)}")
    except Exception as e:
        print(e)

    try:
        print("\nTesting enchantment factory...")
        flaming_factory = enchantment_factory("Flaming")
        frozen_factory = enchantment_factory("Frozen")
        print(flaming_factory("Sword"))
        print(frozen_factory("Shield"))
    except Exception as e:
        print(e)

    try:
        print("\nTesting memory vault...")
        vault = memory_vault()
        print("Store 'secret' = 42")
        key = 'secret'
        value = 42
        vault['store'](key, value)
        print(f"Recall '{key}': {vault['recall'](key)}")
        print(f"Recall 'unknown': {vault['recall']('unknown')}")
    except Exception as e:
        print(e)
