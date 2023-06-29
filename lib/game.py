import random
from .print import game_setup_print, error_print

def get_story_rounds():
    length_map = {
        "1": "20",
        "2": "50",
        "3": "100"
    }


    statement = """
Please choose your story length:

1- Short
2- Medium
3- Long
    """

    game_setup_print(statement)

    # Get input from user
    while True:
        length_input = input()

        if not length_input.strip() in length_map.keys():
            error_print("Your input must be one of 1, 2, or 3")
        else:
            length = length_map[length_input]
            return int(length)
        
def get_story_setting():
    statement = """
Please input your story setting (castle, village, abandoned house, space, island, etc...)
leave blank if you want the AI to select a random setting:
    """

    game_setup_print(statement)

    user_input = input()

    if not user_input.strip():
        return None
    return user_input

def get_story_theme():
    statement = """
Please input your story theme (escape, survival, romance, etc...)
leave blank if you want the AI to select a random theme:
    """

    game_setup_print(statement)

    user_input = input()

    if not user_input.strip():
        return None
    return user_input

def get_side_characters():
    add_more_characters_statement = """
If you would like to add more, please describe another character, else type 'no'.
    """

    statement = """
Please input a side character that you would like to insert into the story, describe your character briefly such as your relationship to them, their age, profession etc...
Valid input example is "Emily, My Spouse, age 24, doctor"
leave blank if you do not want to insert a side character:
    """

    game_setup_print(statement)

    characters = []

    while True:
        user_input = input()
        if not user_input.strip():
            return [] # No characters are added
        elif (user_input.lower() == 'no'):
            return characters
        characters.append(user_input)

        game_setup_print(add_more_characters_statement)

def get_narration_mechanism():
    mechanism_map = {
        "1": "free_text",
        "2": "choice_based",
    }


    statement = """
Please choose your narrative type
1- Free text:       Resembles an old school text based adventure where you type your action to advance the plot
2- Choice based:    Choose your action based on a list of choices to advance the plot
    """

    game_setup_print(statement)
        
    # Get input from user
    while True:
        mechanism_input = input()

        if not mechanism_input.strip() in mechanism_map.keys():
            error_print("Your input must be one of 1, or 2")
        else:
            mechanism = mechanism_map[mechanism_input]
            return mechanism

def get_side_characters_w_occurrence(story_rounds, side_characters):
    rounds = story_rounds - 1 # Do not insert character in the last round

    def decrease_by_percentage(value, percentage):
        return round(value - value * percentage)

    # The shorter the length, the higher the percentage and vice versa
    def get_decrease_percentage(length):
        percentage = 100 / (0.1 * length + 1)
        return round(percentage * 0.01, 2)

    numbers= list(range(1, rounds + 1))
    weights = [5 for _ in range(len(numbers))]
    decrease_percentage = get_decrease_percentage(len(side_characters))

    weights[0] = 0 # Do not insert character in the first round

    result = []

    for character in side_characters:
        random_number = random.choices(numbers, weights, k = 1)[0]
        random_number_i = numbers.index(random_number)
        # Decrease the weight of the random number to make it unlikely to be selected in next iteration (if there is)
        weights[random_number_i] = decrease_by_percentage(weights[random_number_i], decrease_percentage)

        result.append({"character": character, "occurrence": random_number})

    return result

# Returns available side characters for round X, X is the current round number
def get_round_side_characters(story_rounds, side_characters):
    return list(filter(lambda x: x["occurrence"] == story_rounds, side_characters))