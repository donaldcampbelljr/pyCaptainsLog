# import json
import math

import google.generativeai as genai
import os

from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

from random_generators import generate_planet_information, generate_generic_event, roll_die, sum_dice_rolls, \
    comparison_dice
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich import print
from rich.console import Console
from main import parse_user_input
from ship import *
from starsystem import *
#
def main():

    GOOGLE_API_KEY = None
    try:
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    except KeyError:
        raise KeyError
    

    def get_gemini_reponse(input):
        #response = chat.send_message(input,stream=False, safety_settings={'HARM_CATEGORY_HARASSMENT':'block_none'})

        ## this allows us to have combat without tripping the safety mechanism,e.g. "Fire all phasers!" would sometimes trigger it.
        response = chat.send_message(input, stream=False,
                                        safety_settings={'HARM_CATEGORY_HARASSMENT': 'BLOCK_ONLY_HIGH'})


        return response

    
    # This is a combat mission example using cards (items) that the ship has gained.
    starting_location = load_starsystem_yaml("sol.yaml")
    starting_location = create_starsystem_from_dict(starting_location)

    current_system = starting_location
    ship = Ship(name="Reliant", location=current_system)

    planet_name = "Tau Ceti"

    planet_dict = generate_planet_information(planet_name)

    spawned_event = generate_generic_event()

    health = ship.health
    enemy_health = 20
    enemy_attribute = "strength"  # if you play a card against this attribute, you get the full bonus? otherwise, you get half the bonus?
    enemy_attribute_power = 5

    initial_input = (f"Let us roleplay. I am a Captain of the {ship.name} on a mission of combat in the System {planet_name}."
                     f"You should pretend you are a hostile Alien in the {planet_name}. My ship has {health} health. Your alien ship has {enemy_health} health."
                     f"Please keep all responses to 2 sentences maximum. Every time I play card (starting with the next input) I want you to narrate the battle.")
    
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    response = get_gemini_reponse(initial_input)
    event_text = response.text


    console = Console()
    console.clear()
    console.print("\n")
    console.rule(f"\n[bold red]System: {planet_name} Planet: {planet_name}")
    
    #player_ship.cargo.update({item['name']:desc})

    player_input = None
    selection = None
    while player_input != 'leave':
        layout = Layout()
        layout.split_column(
            Layout(name="upper"),
            Layout(name="middle"),
            Layout(name="lower")
        )

        layout["middle"].split_row(Layout(name="middleleft"),Layout(name="middleright"),)

        layout["middleleft"].ratio = 2

        layout["middleright"].split_column(Layout(name="Health"), Layout(name="EnemyHealth"))

        selection = event_text


        spawned_event_text = Text(selection)


        layout["middleleft"].update(
            Panel(spawned_event_text, title="EVENT", subtitle="Combat")
        )

        layout["lower"].ratio = 2
        layout["lower"].split_row(
            Layout(name="left"),
            Layout(name="middle1"),
            Layout(name="middle2"),
            Layout(name="right"),
        )

        if "name" in planet_dict:
            upper_text = Text(f"You've entered into orbit of the planet {planet_name}", style="cyan3")
        if "description" in planet_dict:
            upper_text.append(planet_dict["description"]+"\n", style="dark_turquoise")

        if upper_text is None:
            upper_text = Text(f"You've entered the orbit of an unknown planet.")

        layout["upper"].update(upper_text)

        health_progress = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )

        task1 = health_progress.add_task("[green]Health", total=2)
        task2 = health_progress.add_task("[magenta]Crew", total=2)
        task3 = health_progress.add_task("[cyan]Science", total=2)

        health_progress.update(task1, advance=1)
        health_progress.update(task2, advance=0.5)
        health_progress.update(task3, advance=0.9)

        enemy_progress = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )

        enemy_task1 = enemy_progress.add_task("[green]Health", total=2)
        enemy_progress.update(enemy_task1, advance=1)

        layout["Health"].update(
            Panel(health_progress, title="HEALTH"),
        )

        layout["EnemyHealth"].update(
            Panel(enemy_progress, title="ENEMY HEALTH"),
        )

        cards = generate_cards_dumb()

        card_types = ['science', 'combat', 'diplomacy']

        item_titles = []
        item_descs = []
        item_type = []
        item_power = []

        for i in range(6):
            key, val = random.choice(list(cards.items()))
            item_titles.append(key)
            item_descs.append(val)
            item_type.append(random.choice(card_types))
            item_power.append(random.randint(1,7))

        command_text = Text("LEAVE ORBIT: `leave`\n", style="deep_pink1")
        command_text.append("USE CARD: `#1 or #2 or #3`", style="bright_cyan")

        layout["left"].update(
            Panel(item_descs[0], title=item_titles[0], subtitle=item_type[0])
        )
        layout["middle1"].update(
            Panel(item_descs[1], title=item_titles[1], subtitle=item_type[1])
        )

        layout["middle2"].update(
            Panel(item_descs[2], title=item_titles[2], subtitle=item_type[2])
        )

        ship_attributes_text = Text(f"STRENGTH: {ship.strength}\nSCIENCE: {ship.science}\nDIPLOMACY: {ship.diplomacy}")
        enemy_attributes_text = Text(
            f"Attribute: {enemy_attribute}\nPower: {enemy_attribute_power}")

        layout["right"].split(
            Layout(Panel(ship_attributes_text, title="SHIP ATTRIBUTES")),
            Layout(Panel(enemy_attributes_text, title="ENEMY ATTRIBUTES")),
            Layout(Panel(command_text, title="COMMANDS"))
        )

        print(layout)

        player_input = input("Your Orders, Captain? > ")
        verb, noun, extra = parse_user_input(player_input)

        LEAVE_COMMANDS = ["l", "le", "leave"]
        GET_COMMANDS = ["g", "get", "GET", "ge"]

        if verb in LEAVE_COMMANDS:
            console.clear()
            console.print("[bold red]Leaving Orbit...")
            input("> ")
            break
        try:
            sel = int(verb)

            if sel <= len(item_titles):
                # "use card"
                console.clear()
                console.print(f"Using {item_titles[sel]}")
                response = get_gemini_reponse(f"I play this card: {item_titles[sel]} with info {item_descs[sel]} and power {item_type[sel]} {item_power[sel]}. Narrate how this affects the battle.")
                event_text = response.text

                power = []
                combat_text =[]
                # Calculate some dice rolls.
                print(ship[enemy_attribute])
                if item_type[sel] == enemy_attribute:
                    power.append(item_power[sel])
                else:
                    power.append(math.ceil(item_power[sel]/2))

                #This is lazy right now
                if enemy_attribute == "strength":
                    power.append(ship.strength) #need to determine that strength is the right one to use
                if enemy_attribute == "science":
                    power.append(ship.science) #need to determine that strength is the right one to use
                if enemy_attribute == "diplomacy":
                    power.append(ship.diplomacy)  # need to determine that strength is the right one to use


                final_sum = sum_dice_rolls(power)
                combat_text.append(f"Dice Rolls: {power}  Final Sum: {final_sum}")

                if comparison_dice(final_sum, enemy_attribute_power):
                    enemy_health = enemy_health - (final_sum-enemy_attribute_power)
                    combat_text.append(f"  Enemy health is now: {enemy_health}")
                else:
                    combat_text.append("  No hit. Enemy Health is Unchanged!!!!")

                if enemy_health <= 0:
                    console.clear()
                    console.print("ENEMY DESTROYED")
                    input(">")

        except:
            pass

def generate_cards_dumb():

    items = {}
    items.update({"Biomod Printer":"Prints and installs custom biological modifications."})
    items.update({"Zero-Point Converter":"Harnesses energy between dimensions, granting temporary power with unpredictable consequences."})
    items.update({"Sentient Holotape":"Data storage containing a digitized consciousness, eager to share forbidden knowledge."})
    items.update({"Stasis Grenade":"Suspends objects and people in frozen time for tactical escapes or interrogations."})
    items.update({"Neural Weaver":"Helmet for telepathic communication and manipulation, risking permanent consciousness merging."})
    items.update({"Gene Weaver Serum":"Grants temporary access to alien abilities at the cost of potential side effects."})
    items.update({"Quantum Compass":"Points to probabilities or potential futures, guiding through uncertain choices."})

    return items


if __name__ == "__main__":
    main()
