class Shields(object):
    SHIELDS_COST = [125, 100,
                   20, 30,
                   40, 60,
                   80, 100]

    SHIELDS_MAX_LEVEL = 8

    def __init__(self, shields_level):
        self.shields_level = shields_level

    def upgrade(self):
        self.shields_level += 1

    def get_layers(self):
        return self.shields_level / 2;

    def next_layer_cost(self):
        if self.shields_level == 0:
            return SHIELDS_COST[self.shields_level]

        if self.shields_level >= self.SHIELDS_MAX_LEVEL:
            raise "Cannot upgrade shields system anymore"

        cost = self.SHIELDS_COST[self.shields_level]
        if self.shields_level % 2 == 0:
            cost += self.SHIELDS_COST[self.shields_level]

        return cost

class Engines(object):
    # Please not, at position 2, which is worth 15 scrap
    # it means, that to upgrade from level 2 to 3,
    # one needs 15 scrap
    ENGINES_COST = ["NOT POSSIBLE TO UPGRADES ENGINES FROM 0",
            10, 15, 30, 40, 60,
            80, 120]

    ENGINES_EVASION = [0,
            5, 10, 15, 20, 25,
            28, 31, 35]

    ENGINES_MAX_LEVEL = 8

    def __init__(self, engines_level):
        self.engines_level = engines_level

    def upgrade(self):
        self.engines_level += 1

    def next_level_cost(self):
        if self.engines_level >= self.ENGINES_MAX_LEVEL:
            raise "Cannot upgrade engines anymore"
        return self.ENGINES_COST[self.engines_level]

    def get_evasion(self):
        return self.ENGINES_EVASION[self.engines_level]

class Power(object):
    POWER_COST = ["NOT POSSIBLE TO UPGRADE POWER FROM 0",
            30, 30, 30, 30, 30,
            20, 20, 20, 20, 20,
            25, 25, 25, 25, 25,
            30, 30, 30, 30, 30,
            35, 35, 35, 35, 35]

    def __init__(self, power_level, free_power):
        self.power_level = power_level
        self.free_power = free_power

    def free_power(self):
        return self.free_power

    def next_bar_cost(self):
        return self.POWER_COST(self.power_level)

class Ship(object):
    def __init__(self, shields, engines, power):
        self.shields = shields
        self.engines = engines
        self.power = power

    def manned_bonus(self):
        return 5

    def get_shields_layers(self):
        return self.shields.get_layers()

    def next_shields_level_cost(self):
        return self.shields.next_layer_cost()

    def next_engines_level_cost(self):
        return self.engines.next_level_cost()

    def get_free_power(self):
        return self.power.free_power

    def get_evasion(self):
        return self.engines.get_evasion() + self.manned_bonus()

    def upgrade_shields(self):
        self.shields.upgrade()

    def upgrade_engines(self):
        self.engines.upgrade()

def permutation(n):
    if n <= 1:
        return 1

    return n * permutation(n-1)

def chance_to_get_hit_by_at_least_one_laser(shield_layers, evasion, projectiles):
    layers = shield_layers

    if layers >= projectiles:
        return 0

    if layers < 0:
        layers = 0

    if projectiles <= 0:
        return 1

    hit = (100 - evasion) / 100.0
    hit *= chance_to_get_hit_by_at_least_one_laser(layers - 1, evasion, projectiles - 1)


    miss = (evasion) / 100.0
    miss *= chance_to_get_hit_by_at_least_one_laser(layers, evasion, projectiles - 1)

    return hit + miss

def shields_or_engines(ship):
    shields_next_level_cost = ship.next_shields_level_cost()
    engines_next_level_cost = ship.next_engines_level_cost()
    free_power = ship.get_free_power()
    current_evasion = ship.get_evasion()
    print("Next shield layer cost: " + str(shields_next_level_cost))
    print("Next engines cost: " + str(engines_next_level_cost))
    print("You have free power: " + str(free_power))
    print("Your current evasion: " + str(current_evasion))

    print("Chance of being hit with laser like projectiles at least once:")
    for i in range(1, 10):
        chance = chance_to_get_hit_by_at_least_one_laser(ship.shields.get_layers(),
                current_evasion, i)

        print("%2d laser projectiles:  %.2f%%" % (i, chance * 100))

    ship_copy = Ship(ship.shields, ship.engines, ship.power)
    ship_copy.upgrade_engines()

    current_evasion = ship_copy.get_evasion()

    print("Evasion after upgrade: " + str(current_evasion))
    print("Chance of being hit with laser like projectiles after engine upgrade at least once:")
    for i in range(1, 10):
        chance = chance_to_get_hit_by_at_least_one_laser(ship_copy.shields.get_layers(),
                current_evasion, i)

        print("%2d laser projectiles:  %.2f%%" % (i, chance * 100))

    ship_copy = Ship(ship.shields, ship.engines, ship.power)
    ship_copy.upgrade_shields()
    ship_copy.upgrade_shields()

    print("Chance of being hit with laser like projectiles after shield upgrade at least once:")
    for i in range(1, 10):
        chance = chance_to_get_hit_by_at_least_one_laser(ship_copy.shields.get_layers(),
                current_evasion, i)

        print("%2d laser projectiles:  %.2f%%" % (i, chance * 100))



shields_lvl_01 = 4
test_shields_01 = Shields(shields_lvl_01)

engines_lvl_01 = 2
test_engines_01 = Engines(engines_lvl_01)

power_lvl_01 = 6
free_power_01 = 2
power_01 = Power(power_lvl_01, free_power_01)

ship_01 = Ship(test_shields_01, test_engines_01, power_01)


shields_or_engines(ship_01)

