from collections.abc import Callable
from typing import Any
from functools import wraps
import time


def spell_timer(func: Callable) -> Callable:
    if not callable(func):
        raise TypeError("func must be callable")

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print(f" Casting {func.__name__}...")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f" Spell completed in {end - start:.3f} seconds")
        return result
    return wrapper


def power_validator(min_power: int):
    if not isinstance(min_power, int):
        raise TypeError("min_power must be an int")

    def decorator(func: Callable) -> Callable:
        if not callable(func):
            raise TypeError("func must be callable")

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            power = kwargs.get('power') or args[-1]
            if not isinstance(power, int):
                raise ValueError(" power must be an int")
            if power >= min_power:
                return func(*args, **kwargs)
            return " Insufficient power for this spell"
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> Callable:
    if not isinstance(max_attempts, int) or max_attempts < 1:
        raise ValueError("max_attempts must be an int >= 1")

    def decorator(func: Callable) -> Callable:
        if not callable(func):
            raise TypeError("func must be callable")

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print(f" Spell failed, retrying... "
                              f"(attempt {attempt}/{max_attempts})")
                    attempt += 1
            return f" Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator


class MageGuild:

    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if not isinstance(name, str):
            raise ValueError("name must be a str")
        return len(name) >= 3 and all(c.isalpha() or c == " " for c in name)

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        if not isinstance(spell_name, str) and not isinstance(power, int):
            raise ValueError("name must be a str and power must be an int")
        return f" Successfully cast {spell_name} with {power} power"


@spell_timer
def fireball() -> str:
    time.sleep(0.2)
    return "Fireball cast!"


@retry_spell(3)
def spell() -> None:
    raise Exception('Erreur')


@power_validator(min_power=10)
def is_valid_power(power: int) -> str:
    if not isinstance(power, int):
        raise ValueError("power must be an int")
    return f" {power} power."


if __name__ == '__main__':
    try:
        print("\nTesting spell timer...")
        print(f" Result: {fireball()}")
    except Exception as e:
        print(e)

    try:
        print("\nTesting power validator...")
        print(is_valid_power(1))
        print(is_valid_power(11))
    except Exception as e:
        print(e)

    try:
        print("\nTesting retrying spell...")
        print(spell())
    except Exception as e:
        print(e)

    try:
        print("\nTesting MageGuild...")
        mage_guild = MageGuild()
        print('', mage_guild.validate_mage_name('Alex123'))
        print('', mage_guild.validate_mage_name('Sage'))
        print(mage_guild.cast_spell('shield', 29))
        print(mage_guild.cast_spell('tsunami', 5))
    except Exception as e:
        print(e)
