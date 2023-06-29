from termcolor import cprint

game_setup_print = lambda x: cprint(x, "light_yellow")
error_print = lambda x: cprint(x, "red")
narrator_print = lambda x: cprint(x, "yellow", "on_black", end='')
player_print = lambda x: cprint(x, "green")
game_end_print= lambda x: cprint(x, 'black', 'on_light_yellow', attrs=["bold", "underline"])
