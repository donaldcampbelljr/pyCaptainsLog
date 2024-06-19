import random
import os

from random_generators import get_intro_text
from resources.systems import star_system_descriptions
from starsystem import load_random_values, create_events, StarSystem, save_star_system
from planet import Planet
from event import Event


def generate_systems(web, game_path, start):

    # For each system name in the web, generate a system

    # Then save each system to disk

    # Finally save the "map"/web to disk as well.
    print(f" Here is the input parameters: {web} \n {game_path}")

    starting_system = None

    for name in list(web.keys()):
        starsystem = create_random_starsystem(name, linked_systems=web[name])
        if name == start:
            starting_system = starsystem
        save_star_system(starsystem, game_path)

    return starting_system


def generate_intro_text_local():
    pass


def generate_planets_local():
    pass


def generate_events_local():
    pass


def generate_starsystem_content():

    intro_text = generate_intro_text_local()
    planets = generate_planets_local()
    events = generate_events_local()

    return (
        intro_text,
        planets,
        events,
    )


def create_random_starsystem(name, linked_systems):

    intro_text, planets, events = generate_starsystem_content()

    # values = load_random_values()
    #
    # events = create_events(name=values[0], planets=values[1], alien=values[2])

    # linked_systems = [source_system]

    starsystem = StarSystem(
        name=name,
        planets=planets,
        alien=None,
        linked_systems=linked_systems,
        intro_text=intro_text,
        events=events,
        planets_unlocked=False,
    )

    # save_star_system(starsystem)

    print(f"HERE IS A STAR SYSTEM {starsystem}")

    return starsystem


def build_universes_locally():
    """
    Builds the game universe without using any GPT APIs

    returns a single name, the starting system

    """

    game_path = make_directory()

    # generate list of names

    names = list(star_system_descriptions.keys())

    # connect them as edges to create web for player to traverse

    # For now, make simple closed graph with a start, an end, and 2 systems connected in between
    web, start_system_name, end_system_name = create_web(names)

    starting_system = generate_systems(web, game_path, start_system_name)

    return starting_system


def create_web(names):

    # Cheating for now

    web = {}

    start = random.choice(names)
    names.remove(start)

    web[start] = {}

    end = random.choice(names)
    names.remove(end)

    web[end] = {}

    for i in range(2):
        random_name = random.choice(names)
        if random_name not in web[start]:
            web[start][random_name] = {}
            web[random_name] = {start: {}}
            web[random_name] = {end: {}}

    print(web)
    print(list(web.keys()))

    return web, start, end


def make_directory():

    # create a folder with a unique ID
    generated_hash = create_unique_hash()

    script_dir = os.path.dirname(__file__)
    generated_path = os.path.join(
        os.path.dirname(script_dir), "generated_game", generated_hash
    )

    try:
        os.makedirs(generated_path, exist_ok=True)
    except OSError as error:
        print(f"Error creating directory: {error} Does it already exist?")

    return generated_path


def create_unique_hash():
    """Generates a random 10 digit hash string."""
    digits = "0123456789"
    generated_hash = ""
    # Generate 10 random digits
    for _ in range(10):
        generated_hash += random.choice(digits)

    return generated_hash
