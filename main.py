import yaml
from datetime import datetime
from rich import print
from starsystem import save_star_system, jump_to_starsystem, load_starsystem_yaml, create_starsystem_from_dict
from starsystem import StarSystem, clear
import os
from universe import universe_save
from random_generators import roll_die, comparison_dice, get_event_text
from ship import Ship




def main():
    playing = True



    # Initialize Game

    # Do a loading screen, basically ask the user if they are ready to load the galaxy?

    #star_systems = load_starsystem_yaml()

    #new_system = StarSystem(name="a", planets=["Earth", "Mars", "Pluto"], alien = "aliens", linked_systems = ["origin1"], intro_text = f"Welcome to the system!")

    starting_location = load_starsystem_yaml("sol.yaml")
    starting_location = create_starsystem_from_dict(starting_location)

    # Jump to new or old star system:
    current_system = starting_location

    player_ship = Ship(name="Enterprise", location=current_system)

    # from rich.style import Style
    # my_style = Style(color="blue", bold=True)
    clear()
    print(f"\n[dark_goldenrod]{starting_location.name}[/dark_goldenrod]")


    while playing:
        player_ship.location = current_system
        print("\nWhere would you like to jump?")
        count = 0
        print(f"Adjacent Systems:")
        for i in current_system.linked_systems:
            count += 1
            print(f"{count}  {i}  ")

        count +=1
        print(f"{count}  {'Unexplored'}  ")
        print(f"'#':[purple]jump to system[/purple]  'e':[yellow]engage event[/yellow]  'q':[red]quit[/red]  's':[green]save[/green]")
        # print(f"Press 'q' to quit.")
        # print(f"Press 's' to save and quit.")

        next_system = None

        next_system = input("Enter System: ")



        verb, noun, extra = parse_user_input(next_system)

        if verb == 'q':
            playing = False
        elif verb == 's':
                playing = False
                link = universe_save()
                print(f"Quitting. All files saved. Graph produced here: {link}")
        elif verb == 'e':
            # event logic
            if noun =='planet':
                print("placholder for planet event logic")
            else:
                # assume system level
                success = resolve_system_event(current_system, player_ship)

                if success:
                    print("Encounter [green]successful![/green]")
                else:
                    print("Encounter [red]not successful![/red]")
                save_star_system(current_system)
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

    return verb, noun, extra

def resolve_system_event(current_system: StarSystem, ship: Ship):

    # right now there is one system_level event
    clear()

    for k,v in current_system.events['system'].items():
        #print(v)
        if k == 'event_text':
            current_system.events['system'][k] = get_event_text(location=current_system.name, event_type=current_system.events['system']['type'], ship=ship)


    type = current_system.events['system']['type']
    success_num = current_system.events['system']['success_number']
    value = 0

    if type == 'science':
        value = ship.science
    if type == 'diplomacy':
        value = ship.diplomacy
    if type == 'combat':
        value = ship.strength

    print(current_system.events['system']['event_text'])
    success = comparison_dice(roll_die(value), success_num)

    # if successful
    return success


if __name__ == "__main__":
    main()