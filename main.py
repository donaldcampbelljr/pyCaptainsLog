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



        verb, noun, extra = parse_user_input(next_system)

        if verb == 'q':
            playing = False
        elif verb == 's':
                playing = False
                link = universe_save()
                print(f"Quitting. All files saved. Graph produced here: {link}")
        else:
            try:
                next_system = int(verb) #temp holder for now, just assume if int user wants to jump
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

def parse_user_input(input):
    # simple verb noun identifier
    # e.g. explore planet planet a

    #split_input = input.split()
    user_input = input.split()

    user_input = map(str.strip, user_input)

    user_input = list(user_input)

    try:
        verb = user_input[0]
    except IndexError:
        verb = None

    try:
        noun = user_input[1]
    except IndexError:
        noun = None

    try:
        extra = user_input[2:]
        if len(extra)>1:
            extra = ''.join(extra) # if the name the user gives is 2 or more words...
            extra.lower() # lowercase so that all proper names have no spaces and
        elif len(extra) == 1:
            extra = extra[0].lower()
        else:
            extra = None
    except IndexError:
        extra = None

    #user_input = [verb, noun, extra]

    return verb, noun, extra


if __name__ == "__main__":
    main()