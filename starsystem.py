import yaml
import os
from os import walk
from constants import STAR_DIRECTORY
from random_generators import generate_system_name, generate_alien_name, generate_planets_list, get_intro_text

class StarSystem():
    """
    The main class that intializes star systems and is populated with attributes (planets, etc).
    """

    def __init__(self, name, planets, alien, linked_systems, intro_text) -> None:

        # Load Model, feed it inputs and then generate items.

        self.name = name
        self.planets = planets
        self.alien = alien
        self.linked_systems = linked_systems
        self.intro_text = intro_text

        # self.name = "DefaultSystemName"
        # # Mars, Pluto, Alpha Centauri, Etc.
        # self.planets = ["Earth", "Mars", "Pluto"]
        #
        # # Klingons, Killer Robots, etc.
        # self.alien = "DefaultAlienName"
        #
        # self.linked_systems = ["origin1"]
        #
        # self.intro_text = f"Welcome to the {self.name} system!"


    def __str__(self):
        return f"Starsystem {self.name}"



def save_star_system(starsystem):
    # I thought it would be nice to have all star systems in one big yaml.
    # But maybe it is best to have them segregated such that the info is easier to read.

    starsystem_dict = {}

    # This is clunky, should just make StartSystem class a MutableMapping that has keys...
    if starsystem.name:
        starsystem_dict.update({"StarSystemName": starsystem.name})
    if starsystem.planets:
        starsystem_dict.update({"planets": starsystem.planets})
    if starsystem.alien:
        starsystem_dict.update({"alien": starsystem.alien})
    if starsystem.linked_systems:
        starsystem_dict.update({"linked_systems": starsystem.linked_systems})
    if starsystem.intro_text:
        starsystem_dict.update({"intro_text": starsystem.intro_text})

    yaml_obj_to_write = yaml.dump(starsystem_dict)

    path_starsystems =  os.path.abspath(STAR_DIRECTORY)
    # This is incorrect syntax for appending filename to path as a file in the directory: os.path.join(path_starsystems + file_name)
    file_name = starsystem.name + ".yaml"

    file_path = os.path.join(path_starsystems , file_name)

    with open(file_path, 'w',) as f :
        f.write(yaml_obj_to_write)
    
    print("\n Successful Save to File")


    return 0

def load_random_values():
    """
    Just loads random values from already generated text files
    """

    system_name = generate_system_name()
    planets = generate_planets_list()
    alien = generate_alien_name()

    return system_name, planets, alien

def create_random_starsystem(source_system):
    # self.name = name
    # self.planets = planets
    # self.alien = alien
    # self.linked_systems = linked_systems
    # self.intro_text = intro_text

    values = load_random_values()

    linked_systems = [source_system]

    starsystem = StarSystem(name=values[0], planets=values[1], alien=values[2], linked_systems=linked_systems, intro_text=get_intro_text())

    save_star_system(starsystem)

    return starsystem

def jump_to_starsystem(current_system, next_system):

    ## Check if ship location is already at system
    # check if starsystem already exists (the yaml)
    # create new star system as last option.

    print(f"Current System: {current_system}\n")
    print(f"Next System: {next_system}\n")

    if next_system == "unexplored":
        # Now we should create a new star system:
        create_random_starsystem(source_system=current_system.name)
    else:
        path_starsystems = os.path.abspath(STAR_DIRECTORY)
        filenames = []
        for (dirpath, dirnames, filenames) in walk(path_starsystems):
            print(filenames)

        if current_system.name == next_system:
            print("You are already in this system.")

        filename = next_system+".yaml"
        if filename in filenames:
            next_system = load_starsystem_yaml(next_system)
        else:
            print("SYSTEM NOT FOUND")
    return next_system


def load_starsystem_yaml(starsystemname) -> StarSystem:


    path_starsystems =  os.path.abspath(STAR_DIRECTORY)
    # This is incorrect syntax for appending filename to path as a file in the directory: os.path.join(path_starsystems + file_name)
    file_name = starsystemname + ".yaml"

    file_path = os.path.join(path_starsystems , file_name)
    with open(file_path, mode="rt", encoding="utf-8") as file:
        # print("\n")
        # print(yaml.safe_load(file))
        starsystem_loaded = yaml.safe_load(file)
        for k,v in starsystem_loaded.items():
            print(k)
            print(v)

    # Create system from loaded yaml file
    print(starsystem_loaded)

    starsystem = StarSystem(name=starsystem_loaded["StarSystemName"], planets=starsystem_loaded["planets"], alien=starsystem_loaded["alien"], linked_systems=starsystem_loaded["linked_systems"],
                            intro_text=starsystem_loaded["intro_text"])


    return starsystem