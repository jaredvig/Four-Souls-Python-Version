__author__ = "Jared Vigliecca"
__date__ = "3/14/2023"
import sys
import random
import json

######################################################################################################
# CONSTANTS
######################################################################################################
DEFAULT_AI_FILE = "foursoulsplayer"
DEFAULT_AI_LEVEL = 4
DEFAULT_SHOP_PRICE = 10
DEFAULT_STARTING_COINS = 3
DEFAULT_STARTING_LOOT = 3
DEFAULT_STARTING_ITEMS = 0
DEFAULT_STARTING_SHOP_SIZE = 2
DEFAULT_STARTING_ACTIVE_MONSTERS = 2
DEFAULT_LOOT_DRAW_PER_TURN = 1
DEFAULT_LOOT_PLAY_PER_TURN = 1
DEFAULT_BUYABLE_SHOP_ITEMS_PER_TURN = 1
DEFAULT_FIGHTABLE_MONSTERS_PER_TURN = 1
DEFAULT_SOULS_NEEDED_TO_WIN = 4
DEFAULT_CHARACTER_CARDS = "characters.json"
DEFAULT_LOOT_CARDS = "loot_cards.json"
DEFAULT_ITEM_CARDS = "item_cards.json"
DEFAULT_MONSTER_CARDS = "monsters.json"
DEFAULT_BONUS_SOULS = "bonus_souls.json"
DEFAULT_STARTING_ITEMS = "starting_items_dict.json"
###############################################################################
# Human Player Class
##############################################################################
class HumanPlayer():
   pass 

#######################################################
#Class for the characters that keeps track of their health, damage, and other pertinent stats
#######################################################
class Character:
    def __init__(self, health = 2, attack = 1):
        self.health = health
        self.max_health = health
        self.temp_health = 0
        self.default_attack = attack
        self.attack = self.default_attack
        self.charged = False
    def take_damage(self,damage):
        self.health -=damage
    def heal(self,heal_value):
        self.health+=heal_value
        if(self.health>self.max_health+self.temp_health):
            self.health=self.max_health+self.temp_health
    def add_attack(self,added_attack):
        self.attack+=added_attack
    def reset_character_temporary_effects(self):
        self.health = self.max_health
        self.attack = self.default_attack
    def recharge_character(self):
        self.charged = True


#######################################################
#Class for the loot cards that keeps track of their effects
#######################################################
class LootCard:
    def __init__(self,name,description,effect):
        self.name = name
        self.description = description
        self.effect = effect
    def to_string(self):
        return self.name,self.description


#######################################################
#Class for the items that keeps track of their effects, costs, and other pertinent information
#######################################################
class Item:
    def __init__(name, description, cost, use_code):
        print("Make Item")

#######################################################
#Class for the monsters that keeps track of their health, damage, and other pertinent stats
#######################################################
class Monster:
    def __init__(name,description,health,dice,attack,effects,reward,souls):
        print("Make monster")
    def __init__(name,description,type,effects):
        print("Make Event")
    def __init__(name,description,type,effects):
        print("Make Event")

#######################################################
#Class for the whole player character that will be used in the game
#######################################################
class Player_Character:
    #class variables

    #character functions
    def __init__(self,character_card, player):
        self.coins = 0
        self.player_type= player
        character_card.charged = False
        self.character_card = character_card
        self.loot_cards = []
        self.items = []
        self.curses = []
        self.available_attacks = 1
        self.free_loot_card = False
        self.buyable_items = 1
        self.souls = 0
        for item in self.__items:
            item.charged = False
    def draw_loot_card(self,loot_card):
        print("draw loot card")
        self.loot_cards.append(loot_card)


    def add_coins(self,coins):
        self.coins+=coins

    def subtract_coins(self,coins_to_subtract):
        self.coins-=coins_to_subtract

    def add_curse(self, curse):
        self.curses.append(curse)
    def add_item(self,item):
        self.items.append(item)

    def lose_item(self,item):
        self.items.remove(item)

    def end_turn(self):
        self.can_attack = False
        self.free_loot_card = False
        self.can_buy_item = False

    def discard_loot_card(self,loot_card,discarded_loot):
        self.loot_cards.remove(loot_card)


    



################################################################################
# FUNCTIONS
################################################################################
   

def load_player(player_id, module_name = None, level = 1):
    """
    Load up a ComputerPlayer class from the given module. A module of None means 
    a human player.
    """
    class_name = "Player" +str(player_id)+ "Class"

    # if module_name is None, that means we have a human player
    if module_name == None:
        exec(class_name + " = HumanPlayer", globals())
        return HumanPlayer()

    # look for the file specified, see if we have a proper ComputerPlayer
    try:
        exec("from " +module_name+ " import ComputerPlayer as " +class_name, globals())
    except ImportError:
        print("Could not find ComputerPlayer in file \"" +module_name+ ".py\". Exiting.", file=sys.stderr)
        sys.exit(1)

    # make a local pointer to the ComputerPlayer class, and return a new instance
    exec("Player = " +class_name)
    return locals()["Player"](player_id, level)

def parse_command_line_args(args):
    if "-f" in args: ai_file = args[args.index("-f") + 1].rstrip(".py")
    else: ai_file = DEFAULT_AI_FILE
    
    if "-l" in args:
        levels = args[args.index("-l") + 1].split(',')
        if len(levels) == 1: levels = (int(levels[0]), int(levels[0]))
        else: levels = (int(levels[0]), int(levels[1]))
    else: levels = (DEFAULT_AI_LEVEL, DEFAULT_AI_LEVEL)
    players = []
    total_num_players = -1
    if "-p" in args:
        total_num_players = int(args[args.index("-p") + 1])
        if total_num_players < 2 or total_num_players>4: print("please choose 2-4 players"), sys.exit(1)
    else: players = []*total_num_players
    num_ai = -1
    if "-ai" in args:
        num_ai = int(args[args.index("-a") + 1])
        if num_ai > total_num_players: print("Please have less ais, than total players"), sys.exit(1) 
        else:
            for i in range(total_num_players-num_ai):
                players.append(None)
            for i in range(num_ai):
                players.append(ai_file)
    
    if "-mml" in args:
        levels = args[args.index("-l") + 1].split(',')
        if len(levels) == 1: levels = (int(levels[0]), int(levels[0]), int(levels[0]), int(levels[0]))
        else: levels = (int(levels[0]), int(levels[1]), int(levels[2]), int(levels[3]))
    else: levels = (DEFAULT_AI_LEVEL, DEFAULT_AI_LEVEL)
    return(players, levels)

def shuffle(deck):
    random.shuffle(deck)



def play_game(players):
    ###DEFINING GAMEWIDE FUNCTIONS###
    """
    Initiation and main loop for the game
    """
    """
    Initializing all the pertinent decks required.
    """
    monster_deck_file = open(DEFAULT_MONSTER_CARDS)
    monster_deck = json.load(monster_deck_file)
    loot_deck = json.loads(DEFAULT_LOOT_CARDS)
    treasure_deck = json.loads(DEFAULT_ITEM_CARDS)
    characters = json.loads(DEFAULT_CHARACTER_CARDS)
    starting_items = json.loads(DEFAULT_STARTING_ITEMS)
    discarded_loot_deck = []
    discarded_item_deck = []
    discarded_monster_deck = []
    shop = []
    shop_price = DEFAULT_SHOP_PRICE
    active_monsters = []
    #Shuffle all of the decks that need to be randomly drawn from
    shuffle(monster_deck)
    shuffle(loot_deck)
    shuffle(treasure_deck)
    shuffle(characters)

    #give all of our players a random character, and give them the default number of coins and loot cards
    player_characters = []
    for player in players:
        player_character = Player_Character(characters.remove(random.randrange(len(characters))),player)
        player_character.add_coins(DEFAULT_STARTING_COINS)
        for i in range(DEFAULT_STARTING_LOOT):
            player_character.draw_loot_card(loot_deck)
        player_characters.append(player_character)
    player_has_won = False
    
    #CHOOSE PLAYER ORDER HERE!!!!!!!!!!!!!!
    #
    #
    #
    #
    starting_player = 0 #PLACEHOLDER UNTIL A BETTER WAY TO FIND THE STARTING PLAYER IS FOUND
    current_active_player = starting_player
    stack = []

    for i in range(DEFAULT_STARTING_SHOP_SIZE):
        treasure = treasure_deck.remove(random.randrange(len(treasure_deck)))
        shop.append(treasure)
    for i in range(DEFAULT_STARTING_ACTIVE_MONSTERS):
        initial_monster = monster_deck.remove(random.randrange(len(monster_deck)))
        while initial_monster.type != "Monster":
            monster_deck[i].append(active_monster)
            active_monster = monster_deck.remove(random.randrange(len(monster_deck)))
        active_monsters.append(active_monster)
    shuffle(monster_deck)
    
        #Our main loop, goes until a player has won or a tie has happened.
    while(not player_has_won):
        #ALL OF THE WORK BEFORE THE PLAYER CAN DO THINGS ON THEIR TURN
        current_turn_finished = False
        active_player_character = player_characters[current_active_player]
        start_turn(active_player_character)
        #############################################################
        #Active player choice
        while not current_turn_finished:
            active_player_choice = get_active_player_choice(active_player_character)
            #PLAY FREE LOOT CARD, or activate player card
            if active_player_choice == 1:
                loot_card, target = get_loot_card_choice(active_player_character)
                play_loot_card(loot_card,target)
                #PLAY ITEM
            elif active_player_choice == 2:
                item, target = get_item_choice(active_player_character)
                use_item(item,target)
                #ATTACKING MONSTER DECK
            elif active_player_choice == 3:
                attacked_slot = get_attacked_monster(active_player_choice)
                active_monster
                if attacked_slot == 0:
                    covered_slot = get_monster_slot(active_player)
                    uncover_monster(covered_slot)
                    new_monster = monster_deck.remove(0)
                    active_monsters[covered_slot].append(monster_deck.remove(0))

                else:
                    active_monster = active_monsters[attacked_slot].pop()
                
                if active_monster.type == "Monster":
                    print("Monster")
                elif active_monster.type == "Curse":
                    print("Curse")
                    curse = active_monster
                    target = choose_player(active_player_character)
                    target.add_curse(curse)

                
                else: #Card is an event card
                    print("Event")
                    
                

                    

            #Buy Item
            elif active_player_choice == 4:
                print("buy item")

            #End your turn
            elif active_player_choice == 5:
                print("end turn")
                current_turn_finished = True
            #Invalid choice 
            else: print("Sorry, the inputted value is invalid, please try again")
        #######################################
        active_player_character.end_turn()
        current_active_player = (current_active_player+1)%len(players)


        #####Defining game functions
    def start_turn(active_player):
        for item in active_player.items:
            item.charged = True
        active_player.character_card.charged = True
        active_player.can_attack = True
        active_player.free_loot_card = True
        active_player.can_buy_item = True
        active_player.draw_loot_card(loot_deck(0))
   
    def end_turn(active_player):
        active_player.can_attack = False
        active_player.free_loot_card = False
        active_player.can_buy_item = False

    def purchase_item(active_player, shop_index):
        if(shop_index == 0):
            active_player.items.append(treasure_deck.remove[0])
        else:
            active_player.items.append(shop.remove[shop_index-1])
            shop.append(treasure_deck.remove[0])
        active_player.remove_coins(shop_price)

    def discard_card(card,card_type):
        if(card_type == "monster"):
            discarded_monster_deck.append(card)
        elif(card_type == "item"):
            discarded_item_deck.append(card)
        elif(card_type == "loot"):
            discarded_item_deck.append(card)
    def cancel_next_effect():
        stack.pop()
    def get_active_player_choice(player):
        if player.player_type is None: 
            print("What are you going to do this turn?")
            print("Choose 1 for playing a loot card")
            print("Choose 2 for activating an item")
            print("Choose 3 for fighting a monster")
            print("Choose 4 for buying an item")
            print("Choose 5 to end your turn")
            return input()
   
    def priority(player):
        for i in range(len(players)-1):
            player_priority = (player +i+1)%len(players)
            #######PROMPT PLAYER FOR MOVE########
            #######SKIP MEANS RETURN None########
            #######USE CARD##############
            used_card = get_player_input()
            effect = None
            if(used_card == None):
                continue
            else:
                if(type(used_card) is LootCard):
                    effect = play_loot_card(used_card)
                elif(type(used_card) is Item):
                    effect = play_item(used_card)
                else:
                    effect = use_character(used_card)
                stack.append(effect)
                priority(player_priority)
        exec(stack.pop())
    def choose_loot_card(player):
        loot_cards = player.loot_cards
        loot_index = 1
        print("Please choose a loot card:")
        if player.player_type is None:
            for loot_card in loot_cards:
                print("Type ", loot_index, " to use ", loot_card.name)
            return input()
    def play_loot_card(player):
        loot_index = choose_loot_card(player)
        loot_card = player.loot_cards[loot_index-1]
        effects, targets = get_effects_and_targets(loot_card)
        total_effect_string = ""
        for effect in effects:
            for target in targets:
                effect_string = effect,"(",target,");"
                total_effect_string+=effect_string
        return total_effect_string
        
        #USE ALL APPLICABLE LISTS FOR A TARGET
    def choose_target(target_list):
        if player.player_type is None:
            target_index = 1
            for target in target_list:
                print("Type ", target_index, " to target: ", target.name)
            return target_list[input()]
        

        







        

    

        
        




######################################################################################################
# main
######################################################################################################
if __name__ == "__main__":
    print("Hello World")
    player_files, levels  = parse_command_line_args(sys.argv[1:])
    print(player_files)
    print(levels)
    players = []*len(player_files)
    i = 0
    for player_file in player_files:
        players.append(load_player(i,player_file,levels[i]))
        i+=1

    play_game(player_files)




