from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


#Create Black Magic Spells
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 12, 120, "black")

#Create White Magic Spells
cure = Spell("Cure", 12, 620, "white")
cura = Spell("Cura", 18, 1500, "white")
supacure = Spell("Supacure", 50, 6000, "white")


#Create Some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("Mega Elixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, cure, supacure]
player_items = [{"item":potion, "quantity":5},
                {"item":hipotion, "quantity":5},
                {"item":superpotion,  "quantity":5},
                {"item":elixer,  "quantity":5},
                {"item":hielixer,  "quantity":5},
                {"item":grenade,  "quantity":5}]

#Generate our player and an enemy
player1 = Person("Hero", 3005, 65, 300, 34, player_spells, player_items)
player2 = Person("Generic companion #1", 2451, 65, 311, 34, player_spells, player_items)
player3 = Person("Generic companion #2", 2220, 65, 288, 34, player_spells, player_items)

enemy1 = Person("Thug1", 1032, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Bad Guy",12000, 200, 438, 34, enemy_spells, [])
enemy3 = Person("Thug2", 1032, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
#Game session - while true
while running:
    print("===================")
    print("\n")
    print(bcolors.BOLD + "NAME" + (" " *38) + "HP" + (" " * 42) + "MP" + bcolors.ENDC)
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    #Start of battle - Player chooses action
    for player in players:
        print(bcolors.BOLD + bcolors.UNDERLINE + "\n" + player.name +":"+ bcolors.ENDC)
        player.choose_action()
        choice = input("Choose your action:")
        index = int(choice) - 1

        #Action is attack: reduce dmg from enemy
        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)

            print(player.name,"attacked", enemies[enemy].name, "for",dmg, "points of damage.")
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died")
                del enemies[enemy]
        #Action is a spell: choose a spell and reduce dmg from enemy
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic: ")) - 1
            if magic_choice == -1:
                continue

            #Creates damage for the chosen spell
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage(spell.dmg)

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.WARNING + "\nNot enough MP\n"+bcolors.ENDC)
                continue

            #reduced mana
            player.reduce_mp(spell.cost)

            #Differs between white (heal) and black (attack) magic
            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg),"HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name, "deals", magic_dmg, "points of damage to",enemies[enemy].name + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died")
                    del enemies[enemy]

        #Action is Item: open up Item inventory
        elif index == 2:
            player.choose_items()
            item_choice = int(input("Choose item: ")) - 1

            if item_choice == -1:
                continue

            #Use an item
            item = player.items[item_choice]["item"]
            item_quantity = player.items[item_choice]["quantity"]
            if item_quantity > 0:
                item_quantity -= 1
                player.items[item_choice]["quantity"] = item_quantity
            else:
                print(bcolors.WARNING + "None left..." + bcolors.ENDC)
                continue

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name,"heals for", str(item.prop),"HP" + bcolors.ENDC)

            #Incase of elixer - differs between Mega Elixer and regular elixer.
            elif item.type == "elixer":
                if item.name == "Mega Elixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                    print(bcolors.OKGREEN + "\n"+item.name, "fully restores the team's HP/MP" + bcolors.ENDC)
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name, "fully restores HP/MP" + bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name, "deals", item.prop, "points of damage to",enemies[enemy].name + bcolors.ENDC)
                print(enemies[enemy].name + " has died")
                del enemies[enemy]


    #Summary of turn
    # print("-------------------")
    # print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC +"\n")

    #End of battle - checks if enemies/players are dead
    defeated_enemies = 0
    defeated_players = 0
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    #Checks if enemies won
    if defeated_enemies == len(enemies):
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    # Checks if players won
    elif defeated_players == len(players):
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False


    #Enemy turn to attack
    for enemy in enemies:
        enemy_choice = random.randrange(0, len(enemy.actions))

        if enemy_choice == 0:
            target = random.randrange(0, len(players))
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL + enemy.name,"attacks",players[target].name, "for", enemy_dmg, "points of damage", bcolors.ENDC)
            if players[target].get_hp() == 0:
                print(players[target].name + " has died")
                del players[target]

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals",enemy.name +" for", str(magic_dmg),"HP" + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, len(players))
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + enemy.name, spell.name, "'s deals", magic_dmg, "points of damage to",players[target].name + bcolors.ENDC)
                if players[target].get_hp() == 0:
                    print(players[target].name + " has died")
                    del players[target]




   # running = False
