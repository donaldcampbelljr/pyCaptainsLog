import json
import google.generativeai as genai
import os


def main():

    GOOGLE_API_KEY = None
    try:
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    except KeyError:
        print("None")

    if GOOGLE_API_KEY is not None:
        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel('gemini-pro')
        #
        # # Generating JSON for a Random Starship
        # response = model.generate_content(
        #     f"Please generate 1 unique, random Starship for a tabletop RPG, and display its stats, backstory, etc with the output as "
        #     f"a json object. "
        #     f"Include the following in the stats: hull, shields, speed, weapons (only have phasers and torpedos). Do not simply take ideas from Star Trek."
        #     )

        # Asking for singular responses
        # input = """
        #
        # What year does Bladerunner 2049 take place? Please answer with a singular word, with the format being JSON format.
        #
        # """
        # response = model.generate_content(input)

        dmg_phaser_min = 3
        dmg_phaser_max = 9

        dmg_torp_min = 10
        dmg_torp_max = 15

        enemy_health = 0
        player_health = 13

        # input = """
        #
        # Pretend you are an enemy ship and that you can attack me with either phasers (3-9 dmg) or torpedos (10-15 dmg). What do you attack with and much damage does your attack do? Please answer with a singular word for attack and damage but add asentence of descriptive text of the action, with the format being JSON format.
        #
        # """

        input = f"""

        Pretend you are an enemy ship with {enemy_health} health and that you can attack me (I have a ship with {player_health} health) with either 
        phasers ({dmg_phaser_min}-{dmg_phaser_max} dmg) or torpedos ({dmg_torp_min}-{dmg_torp_max} dmg). 
        What do you attack with and much damage does your attack do? 
        Please answer with a singular word for attack and damage but 
        add a sentence of descriptive text of the action, with the format being JSON format. If your health is 0, return only singular destroyed in the description.'

        """

        response = model.generate_content(input,safety_settings={'HARM_CATEGORY_HARASSMENT': 'BLOCK_ONLY_HIGH'})

        print(response.text)
        finaltext = response.text.replace("`", "")
        finaltext = finaltext.replace("python", "")
        finaltext = finaltext.replace("json", "")

        try:
            parsed_dict = json.loads(finaltext)

            for k,v in parsed_dict.items():
                print(f"{k}\n")
                print(f"{v}\n")
        except:
            print("Could not load JSON.")



if __name__ == "__main__":
    main()