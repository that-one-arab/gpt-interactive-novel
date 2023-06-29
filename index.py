from dotenv import load_dotenv
# Load local .env file
load_dotenv()

import json
import os

from halo import Halo

from lib.prompts import prepare_define_story_prompt, prepare_generate_story_prompt, prepare_system_prompt
from lib.gpt import get_gpt_chat_response, get_gpt_response
from lib.print import narrator_print, player_print, game_end_print
from lib.game import get_narration_mechanism, get_side_characters, get_story_setting, get_story_theme, get_story_rounds, get_side_characters_w_occurrence, get_round_side_characters

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

spinner = Halo(spinner='dots')


theme = get_story_theme()
clear_terminal()
setting = get_story_setting()
clear_terminal()
side_characters = get_side_characters()
clear_terminal()
story_rounds = get_story_rounds()
clear_terminal()
mechanism = get_narration_mechanism()
clear_terminal()

with_choices = False
if mechanism == 'choice_based':
    with_choices = True

if (len(side_characters)):
    side_characters = get_side_characters_w_occurrence(story_rounds, side_characters)

print('\n')
spinner.start('Creating your story...')
story_setting_gpt_response = get_gpt_response(prompt=prepare_define_story_prompt(theme, setting), temperature=1.2)

story_setting = json.loads(story_setting_gpt_response)

messages = [
    {"role": "system", "content": prepare_system_prompt()},
    {"role": "user", "content": prepare_generate_story_prompt(story_setting, with_choices)}
]

spinner.stop()

while True:
    clear_terminal()

    # Decrease remaining rounds by 1 on every player prompt
    story_rounds -= 1

    narrator_print('Narrator: \n')
    response = get_gpt_chat_response(messages, print_stream=True, print_func=narrator_print, temperature=0.2)
    messages.append({"role": "assistant", "content": response})

    player_print('\nPlayer: \n')
    player_input = input()

    available_side_chars = get_round_side_characters(story_rounds, side_characters)
    if (len(available_side_chars)):
        for char in available_side_chars:
            player_input+= f". ADD CHARACTER: '{char['character']}'"

    if (story_rounds == 3):
        player_input+= ". DRAW" # Draw the user close to the ending of the game

    if (story_rounds == 1):
        player_input+= ". END" # Finalize the game, resulting in ending it.
    
    messages.append({"role": "user", "content": player_input})

    # End game condition check
    if story_rounds < 1:
        break

game_end_print("\n\nTHE END")
game_end_print("\n\n\nThank you for playing!")
