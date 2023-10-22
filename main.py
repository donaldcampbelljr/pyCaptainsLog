import yaml
from datetime import datetime
from rich import print
from model_loading import load_starsystem_yaml
from starsystem import save_star_system, jump_to_starsystem
from starsystem import StarSystem


def main():

    # Initialize Game

    # Do a loading screen, basically ask the user if they are ready to load the galaxy?

    star_systems = load_starsystem_yaml()

    new_system = StarSystem()

    print(new_system.name)
    
    save_star_system(new_system)

    # Jump to new or old star system:
    current_system =  new_system

    print("Where would you like to jump?\n\n")
    count = 0
    for i in current_system.linked_systems:
        count + 1
        print("Some Linked Systems:\n")
        print(i + "\n")
    
    next_system = None
    while type(next_system) is not int:
        next_system = input("Enter System: ")
        try:
            next_system = int(next_system)
        except:
            pass
        if type(next_system) is not int or next_system > len(current_system.linked_systems) or next_system < 1:
            print("Invalid Jump Coordinates!!!!!")

    jump_to_starsystem(current_system, next_system)

    return 0

if __name__ == "__main__":
    main()