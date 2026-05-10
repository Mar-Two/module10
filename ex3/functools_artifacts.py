from operator import add, mul
from functools import reduce, partial, lru_cache, singledispatch
from typing import Any
from collections.abc import Callable


def spell_reducer(spells: list[int], operation: str) -> int:
    if (not isinstance(spells, list) or
            not all(isinstance(x, int) for x in spells)):
        raise ValueError("Error: spells must be a list of int")
    if not spells:
        return 0
    operations: dict[str, Callable[[int, int], int]] = {
        "add": add,
        "multiply": mul,
        "max": max,
        "min": min,
    }
    if operation not in operations:
        raise ValueError("Error: Unknown operation")
    return reduce(operations[operation], spells)


def base_enchantment(power: int, element: str, target: str) -> str:
    if (not isinstance(power, int) or
            not isinstance(element, str) or
            not isinstance(target, str)):
        raise ValueError("Error: power must be an int, element must "
                         "be a str and target must be a str")
    return f"{element} enchantment on {target} with {power} power"


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    if not callable(base_enchantment):
        raise TypeError("Error: base_enchantment must be a callable")
    func_1 = partial(base_enchantment, 50, 'Flowing')
    func_2 = partial(base_enchantment, 50, 'Flaming')
    func_3 = partial(base_enchantment, 50, 'Earthen')
    return {
        'func_1': func_1,
        'func_2': func_2,
        'func_3': func_3
    }


def spell_dispatcher() -> Callable[[Any], str]:

    @singledispatch
    def base_dispatch(data: Any) -> str:
        return "Unknown spell type"

    @base_dispatch.register(int)
    def _(data: int) -> str:
        return f"Damage spell: {data} damage"

    @base_dispatch.register(str)
    def _(data: str) -> str:
        return f"Enchantment: {data}"

    @base_dispatch.register(list)
    def _(data: list) -> str:
        return f"Multi-cast: {len(data)} spells"
    return base_dispatch


@lru_cache(maxsize=128)
def memoized_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return memoized_fibonacci(n-1) + memoized_fibonacci(n-2)


if __name__ == '__main__':
    try:
        print('Testing spell reducer...')
        print(f"Sum: {spell_reducer([50, 60, 40, 20], 'add')}")
        print(f"Product: {spell_reducer([50, 60, 40, 20], 'multiply')}")
        print(f"Max: {spell_reducer([50, 60, 40, 20], 'max')}")
        print(f"Min: {spell_reducer([50, 60, 40, 20], 'min')}")
    except Exception as e:
        print(e)

    try:
        print('\nTesting memoized fibonacci...')
        lst_fibo = [0, 1, 10, 15]
        for lst in lst_fibo:
            if not isinstance(lst, int):
                raise ValueError('Error: n must be an int')
            if lst < 0:
                raise ValueError('Error: n must be an int and >= 0')
            print(f"Fib({lst}): {memoized_fibonacci(lst)}")
        print(memoized_fibonacci.cache_info())
    except Exception as e:
        print(e)

    try:
        print('\nTesting partial enchanter...')
        spells = partial_enchanter(base_enchantment)
        print(spells["func_1"]("Wizard"))
        print(spells["func_2"]("Dragon"))
        print(spells["func_3"]("Goblin"))
    except Exception as e:
        print(e)

    try:
        print('\nTesting spell dispatcher...')
        dispatcher = spell_dispatcher()
        print(f"{dispatcher(42)}")
        print(f"{dispatcher('earthquake')}")
        print(f"{dispatcher(['earthquake', 'blizzard', 'freeze', 'shield'])}")
        print(f"{dispatcher(3.0)}")
    except Exception as e:
        print(e)
