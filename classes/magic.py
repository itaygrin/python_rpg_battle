import random


class Spell:
    def __init__(self, name, cost, dmg, type):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.type = type

    def generate_damage(self, dmg):
        low = dmg - 15
        high = dmg + 15
        return random.randrange(low, high)
