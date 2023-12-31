import yaml
from datetime import datetime
from rich import print
from starsystem import save_star_system, jump_to_starsystem, load_starsystem_yaml, create_starsystem_from_dict
from starsystem import StarSystem
import os
from universe import universe_save

def main():
    playing = True

    # Initialize Game

    # Do a loading screen, basically ask the user if they are ready to load the galaxy?

    #star_systems = load_starsystem_yaml()

    #new_system = StarSystem(name="a", planets=["Earth", "Mars", "Pluto"], alien = "aliens", linked_systems = ["origin1"], intro_text = f"Welcome to the system!")

    starting_location = load_starsystem_yaml("sol.yaml")
    starting_location = create_starsystem_from_dict(starting_location)

    print(starting_location.name)

    # Jump to new or old star system:
    current_system = starting_location

    while playing:
        print("Where would you like to jump?\n")
        count = 0
        for i in current_system.linked_systems:
            count += 1
            print(f"Some Linked Systems:")
            print(f"{count}  {i}  ")

        count +=1
        print(f"{count}  {'Unexplored'}  ")
        print(f"Press 'q' to quit.")
        print(f"Press 's' to save and quit.")

        next_system = None

        next_system = input("Enter System: ")

        if next_system == 'q':
            playing = False
        elif next_system == 's':
                playing = False
                link = universe_save()
                print(f"Quitting. All files saved. Graph produced here: {link}")

        else:
            try:
                next_system = int(next_system)
            except:
                pass
            if type(next_system) is not int or next_system > len(current_system.linked_systems)+1 or next_system < 1:
                print("Invalid Jump Coordinates!!!!!")
            if next_system == count:
                next_system = "unexplored"
            else:
                next_system = current_system.linked_systems[count - 2]
            print(next_system)

            next_system = jump_to_starsystem(current_system, next_system)
            current_system = next_system
    return 0

if __name__ == "__main__":
    main()