from rich import print
from rich.console import Console
from rich.table import Table
from starsystem import save_star_system, jump_to_starsystem, load_starsystem_yaml, create_starsystem_from_dict
from starsystem import StarSystem, clear
from universe import universe_save, build_universe_table
from random_generators import roll_die, comparison_dice, get_event_text, chat_event, combat_chat_event, \
    generate_planet_information
from ship import Ship
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout

from constants import PLANET_NOUNS, LEAVE_COMMANDS, GET_COMMANDS
from ship  import build_cargo_table, build_status_table

def main():
    playing = True

    console = Console()

    # Initialize Game
    starting_location = load_starsystem_yaml("sol.yaml")
    starting_location = create_starsystem_from_dict(starting_location)

    current_system = starting_location

    player_ship = Ship(name="Reliant", location=current_system)

    console.clear()




    while playing:
        console.rule(f"\n[dark_goldenrod]{current_system.name}[/dark_goldenrod]")

        print(Panel(current_system.intro_text,))

        if player_ship.health < 0:
            console.clear()
            console.print("[bold red] SHIP DESTROYED")
            console.print("[bold red] Game Over")
            break

        player_ship.location = current_system
        print("\nWhere would you like to jump?")
        count = 0


        adjacent_text = Text("Adjacent Systems")
        for i in current_system.linked_systems:
            count += 1
            adjacent_text.append(f"\n{count}  {i}  ")

        count +=1
        adjacent_text.append(f"\n{count}  {'Unexplored'}  ")
        print(Panel(adjacent_text, title="Adjacent Systems",))

        planet_text = Text("Nearby Planets:")
        for i in current_system.planets:
            planet_text.append((f"\n{i}"))
        print(Panel(planet_text, title="Nearby Planets:", ))

        print(f"'#':[purple]jump to system[/purple]  'e':[yellow]engage event[/yellow]  'status':[cyan]ship status[/cyan] 'systems':[dark_orange]visited systems[/dark_orange] 'q':[red]quit[/red]  's':[green]save[/green]")

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
            if noun in PLANET_NOUNS:
                if extra.title() in current_system.planets:
                    console.clear()
                    # TODO this will not work if the planet name has spaces
                    console.print("[bold red] placeholder for planet event logic")
                    ##print("")
                    planet_name = extra.capitalize()
                    resolve_planet_event(current_system, player_ship, planet_name)
                else:
                    print(f"{extra} is not a nearby planet!")
            else:
                # assume system level
                success = resolve_system_event(current_system, player_ship)

                if success:
                    print("Encounter [green]SUCCESSFUL![/green]")
                else:
                    print("Encounter [red]NOT SUCCESSFUL![/red]")
                save_star_system(current_system)
        elif verb == 'status':
            table = build_status_table(player_ship)
            cargotable = build_cargo_table(player_ship)
            console.clear()
            console.print(table)
            console.print(cargotable)
            input("Press Enter to Continue:")
        elif verb == 'systems':
            table = build_universe_table()
            console.clear()
            console.print(table)
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
            extra = ' '.join(extra) # if the name the user gives is 2 or more words...
        #     extra.lower() # lowercase so that all proper names have no spaces and
        elif len(extra) == 1:
            extra = extra[0].lower()
        # else:
        #     extra = None
    except IndexError:
        extra = None

    return verb, noun, extra


def level_up(ship, type):
    ship.experience += 20
    if type == 'combat':
        ship.strength += 5
    if type == 'science':
        ship.science += 5
    if type == 'diplomacy':
        ship.crew += 5
    if ship.experience > ship.exp_next_level:
        print("LEVEL UP!")
        

def resolve_planet_event(current_system: StarSystem, player_ship: Ship, planet_name: str):


    # print(current_system)
    # print(player_ship)
    # print(planet_name)
    dict = generate_planet_information(planet_name)
    console = Console()
    console.clear()
    console.rule(f"[bold red]System: {current_system.name} Planet: {planet_name}")
    player_input = None
    while player_input != 'leave':


        layout = Layout()
        layout.split_column(
            Layout(name="upper"),
            Layout(name="lower")
        )
        layout["lower"].split_row(
            Layout(name="left"),
            Layout(name="right"),
        )


        upper_text = Text()
        if "name" in dict:
            upper_text.append(f"You've entered into orbit of the planet {planet_name}\n", style="cyan3")
        if "description" in dict:
            upper_text.append(dict["description"]+"\n", style="dark_turquoise")

        if upper_text is None:
            upper_text = Text(f"You've entered the orbit of an unknown planet.")

        layout["upper"].update(upper_text)


        if "items" in dict:
            items_text = Text("")
            # for i in dict["items"]:
            if isinstance(dict["items"], list):
                for item in dict["items"]:
                    if "name" in item:
                        items_text.append(item["name"] + "\n")
                        # also want to make a lowercase version of the name for picking up
                        lc_name = item["name"].lower()
                        lc_name = lc_name.replace(" ", "")
                        item["lcname"] = lc_name
        else:
            items_text = Text("no items")

        command_text = Text("LEAVE ORBIT: `leave`\n", style="deep_pink1")
        command_text.append("GET ITEM: `get xxxxx`", style="bright_cyan")

        layout["right"].split(
            Layout(Panel(items_text, title="ITEMS")),
            Layout(Panel(command_text, title="COMMANDS"))
        )
        layout["left"].update(
            "Other information can go over here."
        )
        print(layout)
        #
        # print(layout.tree)
        player_input = input("Your Orders, Captain? > ")
        verb, noun, extra = parse_user_input(player_input)


        if verb in LEAVE_COMMANDS:
            console.clear()
            console.print("[bold red]Leaving Orbit...")
            input("> ")
            break
        elif verb in GET_COMMANDS:
            if noun:
                found = False
                if "items" in dict:
                    for item in dict["items"]:
                        if "lcname" in item:
                            if noun in item["lcname"]:
                                print(f"GET SUCCESSFUL: {item['name']}")
                                found = True
                                if "description" in item:
                                    desc= item['description']
                                elif "function" in item:
                                    desc = item['function']
                                else:
                                    desc = "Unknown function"
                                player_ship.cargo.update({item['name']:desc})
                if not found:
                    print(f"Scanners do not show, {noun}, in orbit.")


    ## SAVE PLANET INFO AFTER ENGAGEMENT? Or let the player come back whenever and just do it all again?

    return 0



def resolve_system_event(current_system: StarSystem, ship: Ship):

    # right now there is one system_level event
    console = Console()
    console.clear()
    success = False

    for k,v in current_system.events['system'].items():
        if k == 'event_text':
            if 'Placeholder' in current_system.events['system']['event_text']:
                current_system.events['system'][k] = get_event_text(location=current_system.name, event_type=current_system.events['system']['type'], ship=ship)

    type = current_system.events['system']['type']
    success_num = current_system.events['system']['success_number']
    value = 0
    console.rule("[bold red]Encounter Text:")
    console.print(current_system.events['system']['event_text'], justify='center', soft_wrap=True)
    input("Press Enter to Continue: ")

    if type == 'science':
        value = ship.science
        console.rule("[bold red]Attempting Science Event:")
        console.print("[bold red]Outcome:")
        #success = comparison_dice(roll_die(value), success_num)
        success = True
        if success:
            console.print("[bold green]Roll successful!")
            science_event(ship, type, value, current_system.events['system']['event_text'], current_system.name)
        else:
            console.print("[bold red]Roll unsuccessful!")
    if type == 'diplomacy':
        value = ship.diplomacy
        console.rule("[bold red]Outcome:")
        success = comparison_dice(roll_die(value), success_num)
    if type == 'combat':
        value = ship.strength
        console.rule("[bold red]RED ALERT Combat Event:")
        combat_event(ship, type, value, current_system.events['system']['event_text'], current_system.name)
        success = True

    # Perform experience and leveling up here?
    if success:
        level_up(ship, type)

    # if successful
    return success

def science_event(ship, type, value, event_text, system_name):

    # initial_input = (f"I am a Captain of the {ship.name} on a mission of {type} in the System {system_name}. "
    #                  f"You will pretend that you are an Alien in the {system_name} who will submit to questioning by me and my starship crew. "
    #                  f"Please keep all responses to 3 sentences maximum.")

    initial_input = (f"Let us role play in a back and forth conversation where we exchange discussion points. Let us pretend that I am a Captain of the {ship.name} on a mission of {type} in the System {system_name}. "
                     f"You will pretend that you are an Alien in this same system: {system_name}."
                     f"Please keep all responses to 1 sentences maximum.")

    chat_event(initial_input)

    success = True

    return success

def combat_event(ship, type, value, event_text, system_name):

    health = ship.health
    enemy_health = 10
    initial_input = (f"Let us roleplay. I am a Captain of the {ship.name} on a mission of {type} in the System {system_name}."
                     f"You should pretend you are a hostile Alien in the {system_name}. My ship has {health} health. Your alien ship has {enemy_health} health."
                     f"Please keep all responses to 1 sentences maximum. You are able to attack with torpedos or phasers. What do you attack with and how much damamge do you do to my ship?")

    combat_chat_event(initial_input, ship, enemy_health)

    success = True
    return success





if __name__ == "__main__":
    main()