import random
from .magic import Spell

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    #Character Constructor
    def __init__(self,name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)


    #Reduces damage from character
    def take_damage(self, dmg):
        self.hp -= dmg
        if (self.hp <= 0):
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost



    #Choose action menu: presents all options
    def choose_action(self):
        i = 1
        print(bcolors.HEADER + "ACTIONS" + bcolors.ENDC)
        for action in self.actions:
            print("    " + str(i) + ".", action)
            i += 1

    # Choose spell menu: presents all options
    def choose_magic(self):
        i = 1
        print("\n" +bcolors.HEADER + "MAGIC" + bcolors.ENDC)
        for spell in self.magic:
            print("    " + str(i) + ".", spell.name, "(cost:", str(spell.cost) +")")
            i += 1

    # Choose items menu: presents all options
    def choose_items(self):
        i = 1
        print("\n" + bcolors.HEADER + "ITEMS:" + bcolors.ENDC)
        for item in self.items:
            print("    " + str(i) + ".", item["item"].name, ":", item["item"].description, " (x"+ str(item["quantity"]) +")")
            i += 1

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() == 0:
                continue
            print("     " + str(i) + ".", enemy.name)
            i+=1
        choice = (int)(input("Choose target: ")) -1
        return choice

    def get_enemy_stats(self):
        hp_blocks = (int)((self.hp / self.maxhp) * 50)
        hp_spaces = 50 - hp_blocks
        hp_numeric_spaces = " "*(11 - len(str(self.maxhp)) - len(str(self.hp)))
        filler_spaces = (30 - len(self.name)) * " "

        print(bcolors.BOLD + self.name +  ":"+ filler_spaces +
              bcolors.FAIL + str(self.hp) + "/" + str(self.maxhp) + hp_numeric_spaces + "  |"+ "█"*hp_blocks + " "*hp_spaces  + "|       " + bcolors.ENDC)

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_damage(spell.dmg)

        percent = (self.hp/self.maxhp) * 100

        #Enemy AI - if it chooses a healing spell and he has enough HP, he'll rechoose.
        if self.mp < spell.cost or spell.type == "white" and percent > 30:
            self.choose_enemy_spell()       #Recursive call to itself, to reopen the menu of spells incase not enough mp
        else:
            return spell, magic_dmg


    def get_stats(self):
        filler_spaces = (30 - len(self.name)) * " "
        hp_blocks = (int)((self.hp/self.maxhp)*25)
        hp_spaces = 25 - hp_blocks
        mp_blocks = (int)((self.mp/self.maxmp)*10)
        mp_spaces = 10 - mp_blocks
        hp_numeric_spaces = " "*(8 - len(str(self.maxhp)) - len(str(self.hp)))
        mp_numeric_spaces = " "*(6 - len(str(self.maxmp)) - len(str(self.mp)))

        # print("                         _________________________                __________ ")
        print(bcolors.BOLD + self.name +  ":"+ filler_spaces +
              bcolors.OKGREEN + str(self.hp) + "/" + str(self.maxhp) + hp_numeric_spaces + "  |"+ "█"*hp_blocks + " "*hp_spaces  + "|       " + bcolors.ENDC + bcolors.BOLD +
              bcolors.OKBLUE + str(self.mp) + "/"+ str(self.maxmp) + mp_numeric_spaces +"|" + "█"*mp_blocks + " "*mp_spaces + "|" + bcolors.ENDC)

        #(3700 / 4200) * 25 = 22    hp / maxhp *25 blocks = 22 blocks