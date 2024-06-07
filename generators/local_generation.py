import random
import os
from resources.systems import star_system_descriptions


def generate_systems(web, game_path):

    #For each system name in the web, generate a system

    #Then save each system to disk

    # Finally save the "map"/web to disk as well.



    pass


def build_universes_locally():
    """
    Builds the game universe without using any GPT APIs

    """

    game_path = make_directory()

    # generate list of names

    names = list(star_system_descriptions.keys())

    # connect them as edges to create web for player to traverse

    # For now, make simple closed graph with a start, an end, and 2 systems connected in between
    web = create_web(names)

    generate_systems(web, game_path)


    return True


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
            web[random_name] = {start:{}}
            web[random_name] = {end:{}}

    print(web)
    print(list(web.keys()))

    return web


def make_directory():

    # create a folder with a unique ID
    generated_hash = create_unique_hash()

    script_dir = os.path.dirname(__file__)
    generated_path = os.path.join(
        os.path.dirname(script_dir), "generated_game", generated_hash
    )

    try:
        os.mkdir(generated_path)
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
