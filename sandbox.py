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

        response = model.generate_content(
            f"Please generate 1 Starship for a tabletop RPG, and display its stats, backstory, etc with the output as "
            f"a json object. "
            f"Include the following in the stats: hull, shields, speed, weapons (only have phasers and torpedos)."
            )

        print(response.text)
        finaltext = response.text.replace("`", "")
        finaltext = finaltext.replace("python", "")

        parsed_dict = json.loads(finaltext)

        for k,v in parsed_dict.items():
            print(f"{k}\n")
            print(f"{v}\n")



if __name__ == "__main__":
    main()