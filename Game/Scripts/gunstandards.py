SNIPER_VALUES = {
    'Damage': 40,
    'Firerate': 2000,
    'Range': 3000
}

UZI_VALUES = {
    'Damage': 1,
    'Firerate': 1,
    'Range': 1000
}

SHOTGUN_VALUES = {
    'Damage': 12,
    'Firerate': 300,
    'Range': 2000
}

GRENADE_VALUES = {
    'Damage': -60,
    'Firerate': 3000,
    'Range': 3.5
}

GUN_VALUES = {
    0: SNIPER_VALUES,
    1: UZI_VALUES,
    2: SHOTGUN_VALUES,
    3: GRENADE_VALUES
}

def get_gun_damage(gun_type):
    if gun_type < len(GUN_VALUES):
        return GUN_VALUES[gun_type]['Damage']
    return -1

def get_gun_firerate(gun_type):
    if gun_type < len(GUN_VALUES):
        return GUN_VALUES[gun_type]['Firerate']
    return -1

def get_gun_range(gun_type):
    if gun_type < len(GUN_VALUES):
        return GUN_VALUES[gun_type]['Range']
    return -1

def get_gun_property(gun_type, gun_property):
    if gun_type < len(GUN_VALUES):
        return GUN_VALUES[gun_type][gun_property]
    return -1