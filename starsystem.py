import yaml
import os
from os import walk
from os import system, name
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
        name = name.replace(" ", "")
        name = name.lower()
        # Make the string lowercase using th
        self.file_name = name+".yaml"



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
    if starsystem.file_name:
        starsystem_dict.update({"file_name": starsystem.file_name})

    yaml_obj_to_write = yaml.dump(starsystem_dict)

    path_starsystems =  os.path.abspath(STAR_DIRECTORY)
    # This is incorrect syntax for appending filename to path as a file in the directory: os.path.join(path_starsystems + file_name)
    file_name = starsystem.file_name

    file_path = os.path.join(path_starsystems, file_name)

    with open(file_path, 'w',) as f :
        f.write(yaml_obj_to_write)
    
    print("Successful Save to File")


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

    starsystem = StarSystem(name=values[0], planets=values[1], alien=values[2], linked_systems=linked_systems, intro_text=get_intro_text(system_name=values[0]))

    save_star_system(starsystem)

    return starsystem

def jump_to_starsystem(current_system: StarSystem, next_system_name: str,):

    ## Check if ship location is already at system
    # check if starsystem already exists (the yaml)
    # create new star system as last option.

    print(f"Current System: {current_system}\n")

    if next_system_name == "unexplored":
        # Now we should create a new star system:
        next_system = create_random_starsystem(source_system=current_system.name)
        print(f"Next System: {next_system.name}\n")
    else:
        if current_system.name == next_system_name:
            print("You are already in this system.")
            next_system = current_system
            clear()
            print("Successful Jump")
        else:
            path_starsystems = os.path.abspath(STAR_DIRECTORY)
            filenames = []
            for (dirpath, dirnames, filenames) in walk(path_starsystems):
                print(filenames)

            # Convert user facing name to lower case without spaces to find file name.
            next_system_name = next_system_name.replace(" ", "")
            next_system_name = next_system_name.lower()

            filename = next_system_name + ".yaml"

            if filename in filenames:
                next_system = load_starsystem_yaml(filename)
                next_system = create_starsystem_from_dict(next_system)
                clear()
                print("Successful Jump")
            else:
                print("SYSTEM NOT FOUND")
                next_system = current_system
                print("JUMP NOT COMPLETED")

    print(next_system.intro_text)
    return next_system


def load_starsystem_yaml(starsystemfilename) -> StarSystem:


    path_starsystems =  os.path.abspath(STAR_DIRECTORY)
    # This is incorrect syntax for appending filename to path as a file in the directory: os.path.join(path_starsystems + file_name)
    file_name = starsystemfilename

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
    #
    # starsystem = StarSystem(name=starsystem_loaded["StarSystemName"], planets=starsystem_loaded["planets"], alien=starsystem_loaded["alien"], linked_systems=starsystem_loaded["linked_systems"],
    #                         intro_text=starsystem_loaded["intro_text"])


    return starsystem_loaded

def create_starsystem_from_dict(starsystem_loaded):
    starsystem = StarSystem(name=starsystem_loaded["StarSystemName"], planets=starsystem_loaded["planets"], alien=starsystem_loaded["alien"], linked_systems=starsystem_loaded["linked_systems"],
                            intro_text=starsystem_loaded["intro_text"])
    return starsystem


def clear():
    print("\n"*20)
    # # for windows
    # if name == 'nt':
    #     _ = system('cls')
    #
    # # for mac and linux(here, os.name is 'posix')
    # else:
    #     _ = system('clear')
