import yaml
from datetime import datetime
from rich import print
from starsystem import save_star_system, jump_to_starsystem, load_starsystem_yaml
from starsystem import StarSystem


def main():

    # Initialize Game

    # Do a loading screen, basically ask the user if they are ready to load the galaxy?

    #star_systems = load_starsystem_yaml()

    #new_system = StarSystem(name="a", planets=["Earth", "Mars", "Pluto"], alien = "aliens", linked_systems = ["origin1"], intro_text = f"Welcome to the system!")

    starting_location = load_starsystem_yaml("sol")

    print(starting_location.name)

    # Jump to new or old star system:
    current_system =  starting_location

    print("Where would you like to jump?\n\n")
    count = 0
    for i in current_system.linked_systems:
        count += 1
        print(f"Some Linked Systems:\n")
        print(f"{count}  {i}  ")

    count +=1
    print(f"{count}  {'Unexplored'}  ")
    
    next_system = None
    while type(next_system) is not int:
        next_system = input("Enter System: ")
        try:
            next_system = int(next_system)
        except:
            pass
        if type(next_system) is not int or next_system > len(current_system.linked_systems+1) or next_system < 1:
            print("Invalid Jump Coordinates!!!!!")

    if next_system == count:
        next_system = "unexplored"
    else:
        next_system = current_system.linked_systems[count - 1]
    print(next_system)

    jump_to_starsystem(current_system, next_system)

    print("Successfully jumped!")
    return 0

if __name__ == "__main__":
    main()