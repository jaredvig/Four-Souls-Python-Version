__author__ = "Jared Vigliecca"
__date__ = "3/14/2023"
import sys
import random


######################################################################################################
# CONSTANTS
######################################################################################################
DEFAULT_AI_FILE = "foursoulsplayer"
DEFAULT_AI_LEVEL = 4
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

#######################################################
#Class for the monsters that keeps track of their health, damage, and other pertinent stats
#######################################################
class Monster:

#######################################################
#Class for the whole player character that will be used in the game
#######################################################
class Player_Character:
    #class variables

    #character functions
    def __init__(self,character_card,coins = 3,num_loot_cards=3):
        self.coins = coins
        character_card.charged = False
        self.character_card = character_card
        self.num_loot_cards = num_loot_cards
        self.loot_cards = []
        self.items = []
        self.can_attack = False
        self.free_loot_card = False
        self.can_buy_item = False
        self.souls = 0
        for i in range(num_loot_cards):
            self.draw_loot_card()
        for item in self.__items:
            item.charged = False
    def draw_loot_card(self,loot_deck):
        print("draw loot card")
        self.loot_cards.append(loot_deck.remove(0))

    def start_turn(self):
         self.draw_loot_card()
         for item in self.__items:
            item.charged = True
         self.character_card.charged = True
    def add_coins(self,coins):
        self.coins+=coins
    def end_turn(self):
        self.can_attack = False
        self.free_loot_card = False
        self.can_buy_item = False


    



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
        if total_num_players < 2 or total_num_players>4: print("please choose 2-4 players"), exit
    else: players = []*total_num_players
    num_ai = -1
    if "-a" in args:
        num_ai = int(args[args.index("-a") + 1])
        if num_ai > total_num_players: print("Please have less ais, than total players"), exit 
        else:
            for i in range(total_num_players-num_ai):
                players.append(None)
            for i in range(num_ai):
                players.append(ai_file)
    
    if "-l" in args:
        levels = args[args.index("-l") + 1].split(',')
        if len(levels) == 1: levels = (int(levels[0]), int(levels[0]), int(levels[0]), int(levels[0]))
        else: levels = (int(levels[0]), int(levels[1]), int(levels[2]), int(levels[3]))
    else: levels = (DEFAULT_AI_LEVEL, DEFAULT_AI_LEVEL)
    return(players, levels)

def choose_random_player_character():
    print("Random player")


def play_game(players):
    """
    Initiation and main loop for the game
    """


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

    play




