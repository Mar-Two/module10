def validate_dicts(data: list[dict], required_keys: set) -> None:
    if not isinstance(data, list) or not data:
        raise ValueError("Error: data must be a list and len(>=1)")
    for item in data:
        if (not isinstance(item, dict) or
                not required_keys.issubset(item.keys())):
            raise ValueError("Error: Invalid structure. Missing: "
                             f"{required_keys - item.keys()}")
        if ('power' in required_keys and
                not isinstance(item.get('power'), (int, float))):
            raise ValueError("Error: Power must be a number")


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    validate_dicts(artifacts, {'name', 'power', 'type'})
    return sorted(artifacts, key=lambda artifact: artifact['power'],
                  reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    validate_dicts(mages, {'name', 'power', 'element'})
    return list(filter(lambda mage: mage['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    if (not isinstance(spells, list) or
            not all(isinstance(x, str) for x in spells) or not spells):
        raise ValueError("Error: spells must be a list of strings")
    return list(map(lambda s: f"* {s} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    validate_dicts(mages, {'name', 'power', 'element'})
    max_p = max(mages, key=lambda m: m['power'])['power']
    min_p = min(mages, key=lambda m: m['power'])['power']
    total_power = sum(map(lambda m: m['power'], mages))
    avg_p = round(total_power / len(mages), 2)
    return {
        'max_power': int(max_p),
        'min_power': int(min_p),
        'avg_power': float(avg_p)
    }


if __name__ == '__main__':
    try:
        artifacts = artifacts = [{'name': 'Shadow Blade', 'power': 80,
                                  'type': 'weapon'},
                                 {'name': 'Crystal Orb', 'power': 62,
                                  'type': 'armor'},
                                 {'name': 'Light Prism', 'power': 90,
                                  'type': 'weapon'},
                                 {'name': 'Storm Crown', 'power': 81,
                                  'type': 'relic'}]
        print('Testing artifact sorter...')
        func_artifact_sorter = artifact_sorter(artifacts)
        i = 1
        for artifact in func_artifact_sorter:
            print(f"{i}: {artifact['name']} "
                  f"({artifact['power']} power) type {artifact['type']}")
            i += 1
    except Exception as e:
        print(e)

    try:
        print('\nTesting power filter...')
        mages = [{'name': 'Ember', 'power': 93, 'element': 'fire'},
                 {'name': 'Rowan', 'power': 68, 'element': 'shadow'},
                 {'name': 'Storm', 'power': 53, 'element': 'earth'},
                 {'name': 'Storm', 'power': 52, 'element': 'ice'},
                 {'name': 'Alex', 'power': 57, 'element': 'wind'}]
        min_power = 60
        func_power_filter = power_filter(mages, min_power)
        print(f"Mages who have a power of more than {min_power}:")
        i = 1
        for power_filt in func_power_filter:
            print(f"{i}: {power_filt['name']} ({power_filt['power']} power) "
                  f"element {power_filt['element']}")
            i += 1
    except Exception as e:
        print(e)

    try:
        print('\nTesting spell transformer...')
        spells = ['darkness', 'fireball', 'tornado', 'tsunami']
        func_spell_transformer = spell_transformer(spells)
        print(f"{' '.join(func_spell_transformer)}")
    except Exception as e:
        print(e)

    try:
        print('\nTesting mage stats...')
        mages = [{'name': 'Ember', 'power': 93, 'element': 'fire'},
                 {'name': 'Rowan', 'power': 68, 'element': 'shadow'},
                 {'name': 'Storm', 'power': 53, 'element': 'earth'},
                 {'name': 'Storm', 'power': 52, 'element': 'ice'},
                 {'name': 'Alex', 'power': 57, 'element': 'wind'}]
        func_mage_stats = mage_stats(mages)
        for k, v in func_mage_stats.items():
            print(f"{k}={v}")
    except Exception as e:
        print(e)
