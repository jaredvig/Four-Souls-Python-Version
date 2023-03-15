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
    def __init__(self,name,description,code_string):
        self.name = name
        self.description = description
        self.code_string = code_string
    def activate_card_effects(self):
        exec(self.code_string)
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
        self.player= player
        character_card.charged = False
        self.character_card = character_card
        self.num_loot_cards = 0
        self.loot_cards = []
        self.items = []
        self.can_attack = False
        self.free_loot_card = False
        self.can_buy_item = False
        self.souls = 0
        for item in self.__items:
            item.charged = False
    def draw_loot_card(self,loot_deck):
        print("draw loot card")
        self.loot_cards.append(loot_deck.remove(0))
        self.num_loot_cards +=1
    def start_turn(self,loot_deck):
         self.draw_loot_card(loot_deck)
         for item in self.items:
            item.charged = True
         self.character_card.charged = True
    def add_coins(self,coins):
        self.coins+=coins
    def end_turn(self):
        self.can_attack = False
        self.free_loot_card = False
        self.can_buy_item = False
    def discard_loot_card(self,loot_card,discarded_loot):
        self.loot_cards.remove(loot_card)
        self.num_loot_cards -=1


    



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
    current_player = starting_player


    for i in range(DEFAULT_STARTING_SHOP_SIZE):
        treasure = treasure_deck.remove(random.randrange(len(treasure_deck)))
        shop.append(treasure)
    for i in range(DEFAULT_STARTING_ACTIVE_MONSTERS):
        active_monster = monster_deck.remove(random.randrange(len(monster_deck)))
        while active_monster.type != "Monster":
            monster_deck.append(active_monster)
            active_monster = monster_deck.remove(random.randrange(len(monster_deck)))
        active_monsters.append(active_monster)


        #Our main loop, goes until a player has won or a tie has happened.
    while(not player_has_won):

        current_player_character = player_characters[current_player]
        current_player_character.start_turn(loot_deck)
        #######################################
        #
        #WRITE WHAT HAPPENS IN A TURN HERE
        #
        #######################################
        current_player_character.end_turn()
        current_player = (current_player+1)%len(players)


        

    

        
        




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




