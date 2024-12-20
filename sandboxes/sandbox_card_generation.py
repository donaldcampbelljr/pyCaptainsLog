import json
import google.generativeai as genai
import os


def main():

    GOOGLE_API_KEY = None
    try:
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    except KeyError:
        print("None")

    if GOOGLE_API_KEY is not None:
        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel("gemini-pro")

        #         input = f"""
        #         Generate 1 unique planet for a tabletop rpg. Answer in JSON format with primary keys: name, description, planet_type, items.
        #         For items, only generate a max of 3 items. Make sure the theme is science fiction.
        # """

        input = f"""

        Generate 20 unique items for a science fiction tabletop RPG. Answer in JSON format with primary keys: name, description, power. 
        The power should be described as a key value pair e.g. "strength": 5, "science":6, "diplomacy":1. Only use one of the powers (not all three) 
        and make sure the power level is anywhere between 2 and 8.
"""

        response = model.generate_content(
            input, safety_settings={"HARM_CATEGORY_HARASSMENT": "BLOCK_ONLY_HIGH"}
        )

        print("RESPONSE TEXT------------------------")
        print(response.text)
        finaltext = response.text.replace("`", "")
        finaltext = finaltext.replace("python", "")
        finaltext = finaltext.replace("json", "")

        try:
            parsed_dict = json.loads(finaltext)
            print("LOADED JSON------------------------")
            for k, v in parsed_dict.items():
                print(f"{k}\n")
                print(f"{v}\n")
        except:
            print("Could not load JSON.")


if __name__ == "__main__":
    main()
