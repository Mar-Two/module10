from collections.abc import Callable


def heal(target: str, power: int) -> str:
    if not isinstance(target, str) or not isinstance(power, int):
        raise ValueError("target must be a str and power must be an int")
    return f"Heal restores {target} for {power} HP"


def fireball(target: str, power: int) -> str:
    if not isinstance(target, str) or not isinstance(power, int):
        raise ValueError("target must be a str and power must be an int")
    return f"Fireball hits {target} for {power} damage"


def is_condition(target: str, power: int) -> bool:
    if not isinstance(target, str) or not isinstance(power, int):
        raise ValueError("target must be a str and power must be an int")
    return target == 'Wizard' and power >= 15


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    if not callable(spell1) or not callable(spell2):
        raise TypeError('spell1 and spell2 must be callable')
    return lambda target, power: (spell1(target, power), spell2(target, power))


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    if not isinstance(multiplier, int):
        raise ValueError('multiplier must be an int')
    if not callable(base_spell):
        raise TypeError("base_spell must be callable")
    return lambda target, power: base_spell(target, power * multiplier)


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    if not callable(condition) or not callable(spell):
        raise TypeError("condition and spell must be a callable")
    return (lambda target, power: spell(target, power)
            if condition(target, power) else "Spell fizzled")


def spell_sequence(spells: list[Callable]) -> Callable:
    if not all(callable(x) for x in spells):
        raise TypeError("All items in spells list must be callable")
    return lambda target, power: [x(target, power) for x in spells]


if __name__ == '__main__':
    try:
        combined = spell_combiner(fireball, heal)
        print('Testing spell combiner...')
        print(f"Combined spell result: {combined('Dragon', 23)}\n")
    except Exception as e:
        print(e)

    try:
        print('Testing power amplifier...')
        amplified = power_amplifier(heal, 2)
        power = 10
        print(f"Original: {heal('Goblin', 10)}. Amplified: "
              f"{amplified('Goblin', 10)}\n")
    except Exception as e:
        print(e)

    try:
        print('Testing conditional caster...')
        conditional_cast = conditional_caster(is_condition, fireball)
        print(f"{conditional_cast('Wizard', 16)}\n")
    except Exception as e:
        print(e)

    try:
        print('Testing spell sequence...')
        spell_lst = spell_sequence([fireball, heal, fireball, heal])
        print(f"{spell_lst('Knight', 20)}")
    except Exception as e:
        print(e)
