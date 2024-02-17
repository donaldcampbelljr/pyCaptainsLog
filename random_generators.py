import random
import os
import json
import google.generativeai as genai
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from constants import GOOGLE_API_KEY, CARD_TYPES, DIPLOMACY, STRENGTH, SCIENCE
from utils import parse_user_input


def generate_system_name():
    first_syllables = ["Exo", "Aeth", "Xan", "Sol", "Terra", "Bel", "Mar", "Jov", "Neb", "Kep"]
    second_syllables = ["on", "ar", "eth", "ia", "us", "a", " Prime", " Major", " Minor", " Beta"]
    third_syllables = ["is", "os", "a", "or", "on", "ia", " Prime", " Major", " Minor", " Beta"]
    first = random.choice(first_syllables)
    second = random.choice(second_syllables)
    third = random.choice(third_syllables)
    return f"{first}{second}{third}"

def generate_alien_name():
    first_syllables = ["Zyl", "Xheth", "Yth", "Qel", "Vry", "T'eyl", "Khel", "Aethel", "Xylos", "Zyron"]
    second_syllables = ["an", "ar", "en", "in", "ai", "ora", "ryn", "thal", "kar", "nar"]
    third_syllables = ["'ai", "ath", "na", "on", "ya", "ee", "is", "kar", "van", "yr"]
    first = random.choice(first_syllables)
    second = random.choice(second_syllables)
    third = random.choice(third_syllables)
    return f"{first}{second}{third}"

def generate_planets_list():
    list_of_planets = []
    for i in range(random.randint(1, 5)):
        system_name = generate_system_name()
        list_of_planets.append(system_name)
    return list_of_planets

def generate_planet_information(planet_name: str):
    """
    Generates the more detailed info and stats for a planet. If no API key, just provide defaults.
    :return: dict of information about the planet
    """
    console = Console()
    console.clear()
    GOOGLE_API_KEY = None
    try:
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    except KeyError:
        print("None")

    if GOOGLE_API_KEY is not None:
        console.print("[yellow3]ENTERING PLANETARY ORBIT....")
        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel('gemini-pro')

        input = f"""
                Generate 1 unique planet for a tabletop rpg with the name {planet_name}. Answer in JSON format with primary keys: name, description, planet_type, items. For items, only generate a max of 3 items. Make sure the theme is science fiction.
        """

        response = model.generate_content(input)

        print(response.text)
        finaltext = response.text.replace("`", "")
        finaltext = finaltext.replace("python", "")
        finaltext = finaltext.replace("json", "")

        try:
            parsed_dict = json.loads(finaltext)
            # for k, v in parsed_dict.items():
            #     print(f"{k}\n")
            #     print(f"{v}\n")
        except:
            print("Could not load JSON.")
            parsed_dict = {}
            parsed_dict["name"] = planet_name
            parsed_dict["description"] = "place holder description"
            parsed_dict["items"] = "[place holder items]"
    else:
        parsed_dict = {}
        parsed_dict["name"] = planet_name
        parsed_dict["description"] = "place holder description"
        parsed_dict["items"] = "[place holder items]"

    return parsed_dict

def get_intro_text(system_name):

    # First see if the Google API Key is available, else, generate some random text
    console = Console()
    console.clear()
    GOOGLE_API_KEY = None
    try:
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    except KeyError:
        print("None")

    if GOOGLE_API_KEY is not None:
        console.print("[yellow3]JUMPING INTO THE UNKNOWN....")
        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel('gemini-pro')

        response = model.generate_content(f"Write a brief description about the fictional {system_name} star system. Keep it to two lines of text."
                                          )

        intro_line = response.text
    else:
        def random_line(filename):
            """Reads a random line from a text file."""
            with open(filename, 'r') as file:
                lines = file.readlines()
                random_line = random.choice(lines)
                return random_line.strip()

        # Example usage:
        filename = "demo/infos.txt"
        intro_line = random_line(filename)

    return intro_line


def get_intro_outro(system_name, intro_line):
    if GOOGLE_API_KEY is not None:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')

        input = f"""
Pretend that we are writing a tv script for a science fiction show that involves exploring the final frontier. 
Our heroes spaceship, the USS Reliant has just entered the {system_name} system which has this description {intro_line}. 
Write three sentences that act as the intro line to the episode. 
Then write three sentences that act as the last few lines of episode summary told by a character at the end of the 45 min episode. 
Give the output as a JSON with primary keys: "intro_text", "outro_text".
        
"""
        response = model.generate_content(input,safety_settings={'HARM_CATEGORY_HARASSMENT': 'BLOCK_ONLY_HIGH'})
        finaltext = response.text.replace("`", "")
        finaltext = finaltext.replace("python", "")
        finaltext = finaltext.replace("json", "")
        parsed_dict = {}
        try:
            parsed_dict = json.loads(finaltext)
        except:
            parsed_dict = {}

        # console = Console()
        # console.clear()
        # console.rule("[bold red]Encounter Text:")

        intro_story_text = Text("Our story so far...\n", style="green")
        if "intro_text" in parsed_dict.keys():
            for text in parsed_dict["intro_text"]:
                intro_story_text.append(" "+text)

        intro_story_panel= Panel(intro_story_text, title="Intro")
        # console.print(intro_story_panel)

        outro_story_text = Text("Finally...\n", style="green")
        if "outro_text" in parsed_dict.keys():
            for text in parsed_dict["outro_text"]:
                outro_story_text.append(" "+text)

        outro_story_panel= Panel(outro_story_text, title="Outro")
        # console.print(outro_story_panel)

        return intro_story_panel, outro_story_panel, intro_story_text, outro_story_text


def make_cards_from_inventory(cargo):

    ## Select 3 cards at random from cargo

    keys = list(cargo.keys())
    len_keys = len(keys)

    text = Text("", style="blue")

    choices=[]

    for i in range(0,3):
        num = random.randint(0, len_keys-1)
        key = keys[num]
        choices.append(key)
        text.append(str(i) + " " + key + " " + str(cargo[key]["power_level"]) + " " + str(cargo[key]["power_type"]) + " ")

    panel = Panel(text)

    return choices, panel

def get_gemini_reponse(chat, input):
    response = chat.send_message(input, stream=False,
                                    safety_settings={'HARM_CATEGORY_HARASSMENT': 'BLOCK_ONLY_HIGH'})
    return response


def main_system_event(intro_text, outro_text, ship, event_type = None, event_power_level=None):

    console = Console()
    event_power_level = 5
    event_health = 10
    event_type = DIPLOMACY


    if GOOGLE_API_KEY is not None:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=[])

        initial_input = f""" Based on this science fiction intro text {intro_text} and outro text {outro_text}, 
        begin writing a story for this star system. Only provide a couple of lines after evey one of my responses. 
        If I respond that the ship is losing, change the story in a negative light. If I respond that the ship is winning, 
        please change the story to be more positive. You do not need to repeat that the ship is winning or losing. 
        If I respond that the ship is destroys or loses please finish the story accordingly.
        Don't forget to incorporate chat history when telling this story. Make sure to keep the characters consistent throughout the story.
        Now please begin the story.
"""

        response = get_gemini_reponse(chat, initial_input)
        event_text = response.text
        console.print(event_text)
        input(">>")

        while ship.health >=0 or event_power_level >=0:
            choices, card_panel = make_cards_from_inventory(ship.cargo)
            console.print(card_panel)
            verb = None
            ship_event_power = []
            gemini_input = "Nothing to say."
            while not isinstance(verb, int):
                player_input = input("Your Orders, Captain? > ")
                verb, noun, extra = parse_user_input(player_input)
                try:
                    verb = int(verb)
                except:
                    pass
                verb = verb-1
                if verb <0:
                    verb = 0
                if verb > 2:
                    verb =2
            chosen_card = choices[verb]
            console.print(chosen_card)

            ## Collect all of the Power Modifiers
            ship_event_power.append(int(ship.cargo[chosen_card]["power_level"]))
            if event_type == STRENGTH:
                ship_event_power.append(ship.strength)  # need to determine that strength is the right one to use
            if event_type == SCIENCE:
                ship_event_power.append(ship.science)  # need to determine that strength is the right one to use
            if event_type == DIPLOMACY:
                ship_event_power.append(ship.diplomacy)  # need to determine that strength is the right one to use

            final_sum = sum_dice_rolls(ship_event_power)
            console.print(Panel(f"Dice Rolls: {ship_event_power}  Final Sum: {final_sum}"))

            if comparison_dice(final_sum, event_power_level):
                event_health = event_health - (final_sum - event_power_level)
                console.print(Panel(f"  Event remaining: {event_health}"))
                gemini_input = "The ship is winning."
            else:
                console.print(Panel(f"Face palm: Nothing happens. The {ship.name} takes some damage"))
                ship.health = ship.health-5

            if event_health <= 0:
                console.clear()
                console.print("ENEMY DESTROYED")
                input(">")
                return True

            elif ship.health<=0:
                console.clear()
                console.print("The ship must retreat!")
                input(">")
                return False
            else:
                response = get_gemini_reponse(chat, gemini_input)
                event_text = Panel(response.text)
                console.print(event_text)

    console.print("Default Event Successful")
    return True

def get_event_text(location, event_type, ship):
    # TODO consolidate with intro_text generation
    # First see if the Google API Key is available, else, generate some random text

    location = location
    event_type = event_type

    GOOGLE_API_KEY = None
    try:
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    except KeyError:
        print("None")

    if GOOGLE_API_KEY is not None:
        print("ENGAGING EVENT....\n")
        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel('gemini-pro')

        response = model.generate_content(
            f"Write a brief intro about this fictional, science fiction encounter where our starship, the {ship.name} "
            f"engages in a {event_type} encounter at the location: {location}. Keep it to two lines of text."
            )

        event_text = response.text

    else:
        event_text = " Placeholder since no Google API Key was used"

    return event_text


def check_destroyed(event_text):
    if 'destroyed' in event_text:
        return True
    elif 'Destroyed' in event_text:
        return True
    else:
        return False

def chat_event(initial_input):
    console = Console()

    GOOGLE_API_KEY = None
    try:
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    except KeyError:
        print("No GOOGLE_API_KEY SET!")

    if GOOGLE_API_KEY is not None:
        def get_gemini_reponse(input):
            response = chat.send_message(input,stream=False)
            return response


        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=[])

        console.rule("[bold red]Loading Conversation:")
        response = get_gemini_reponse(initial_input)
        #console.print(f"[green]Initial response {response.text}")

        player_input = None

        event_text = response.text
        console.print(f"[green]{event_text}")

        console.print("[blue]How to proceed?")
        while player_input != 'quit':
            player_input = input("> ")
            response = get_gemini_reponse(player_input)
            event_text = response.text
            console.print(f"[green]{event_text}")

        final_response = response.text or "No response given."

    else:
        final_response = " Placeholder since no Google API Key was used"

    return final_response

def combat_chat_event(initial_input, ship, enemy_health):
    console = Console()

    GOOGLE_API_KEY = None
    try:
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    except KeyError:
        print("No GOOGLE_API_KEY SET!")

    if GOOGLE_API_KEY is not None:
        def get_gemini_reponse(input):
            #response = chat.send_message(input,stream=False, safety_settings={'HARM_CATEGORY_HARASSMENT':'block_none'})

            ## this allows us to have combat without tripping the safety mechanism,e.g. "Fire all phasers!" would sometimes trigger it.
            response = chat.send_message(input, stream=False,
                                         safety_settings={'HARM_CATEGORY_HARASSMENT': 'BLOCK_ONLY_HIGH'})


            return response

        def calculate_damage(ship, enemy_health, text):
            import re

            find_ints = re.findall(r"\d+", text)
            if find_ints is not None:
                try:
                    damage = int(find_ints[0])
                except IndexError:
                    damage = 0
            else:
                damage = 0

            if 'your' or 'Your' in text:
                # Get number and subtract from player ship
                ship.health = ship.health - damage

            if 'miss' or 'Miss' or 'missed' in text:
                # don't do anything
                pass

            if 'my' or 'My' or 'I' in text:
                # get number and subtract from enemy ship
                enemy_health = enemy_health - damage

            return enemy_health




        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=[])

        response = get_gemini_reponse(initial_input)

        player_input = None

        event_text = response.text
        console.print(f"[green]{event_text}")

        enemy_health = calculate_damage(ship, enemy_health, response.text)

        console.print("[blue]How to proceed?")
        while player_input != 'quit':
            console.print(f"[dark_red]Enemy: {enemy_health}[/dark_red]  [sea_green2]Ship: {ship.health}[/sea_green2]")
            player_input = input("> ")
            response = get_gemini_reponse(f"Your ship's health is now: {enemy_health} My ship's health is now: {ship.health} " + player_input + "If I am attacking in my previous sentence, how much damage do you take and do you counter attack? If you decide to counterattack, how much damage does my ship take?")
            event_text = response.text
            console.print(f"[green]{event_text}")
            enemy_health = calculate_damage(ship, enemy_health, response.text)
            if check_destroyed(event_text):
                console.print(f"[magenta]Combat finished!! Ship Destroyed!")
                break
            if enemy_health < 0:
                console.print(f"[magenta]Combat finished!! Enemy Destroyed!")
                break
            if ship.health < 0:
                console.print(f"[magenta]Combat finished!! Your ship is destroyed!")
                break
        final_response = response.text or "No response given."

    else:
        final_response = " Placeholder since no Google API Key was used"

    return final_response

def roll_die(num_sides):
    # simply roll the die
    return random.randint(1, num_sides)

def sum_dice_rolls(all_dice):

    final_sum = 0

    for die in all_dice:
        final_sum += roll_die(die)

    return final_sum

def comparison_dice(a, b):
    print(f"COMPARING: {a} vs {b}")
    if a > b:
        return True
    if b > a:
        return False
    if a == b:
        return True

def generate_generic_event():

    event = {}
    event.update({"description": "On the planet Tau Ceti, you discover a hostile alien known as the Orbsaurrians"})
    event.update({"check":{"Combat": 12}})

    return event