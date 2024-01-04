import random
import os
import google.generativeai as genai
from rich import print
from rich.console import Console


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

def get_intro_text(system_name):

    # First see if the Google API Key is available, else, generate some random text

    GOOGLE_API_KEY = None
    try:
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    except KeyError:
        print("None")

    if GOOGLE_API_KEY is not None:
        print("JUMPING INTO THE UNKNOWN....\n")
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

        #console.rule("[bold red]Conversation:")

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
            response = chat.send_message(input,stream=False)
            return response

        def calculate_damage(ship, enemy_health, text):
            import re

            find_ints = re.findall(r"\d+", text)
            if find_ints is not None:
                damage = int(find_ints[0])
            else:
                damage = 0

            if 'your' or 'Your' in text:
                # Get number and subtract from player ship
                ship.health = ship.health - damage

            if 'miss' or 'Miss' or 'missed' in text:
                # don't do anything
                pass

            if 'my' or 'My' in text:
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
            player_input = input("> ")
            response = get_gemini_reponse(f"Your ship's health is now: {enemy_health} My ship's health is now: {ship.health} " + player_input + " How much damage do you take and do you counter attack? If so how much damage do I take?")
            event_text = response.text
            console.print(f"[green]{event_text}")
            enemy_health = calculate_damage(ship, enemy_health, response.text)
        final_response = response.text or "No response given."

    else:
        final_response = " Placeholder since no Google API Key was used"

    return final_response

def roll_die(num_sides):
    # simply roll the die
    return random.randint(1, num_sides)


def comparison_dice(a, b):
    print(f"COMPARING: {a} vs {b}")
    if a > b:
        return True
    if b > a:
        return False
    if a == b:
        return True
