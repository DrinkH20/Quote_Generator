import pyautogui
from PIL import Image
import pytesseract
import pyperclip
import time

from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '100')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'left', 20)
Config.set('graphics', 'top', 50)
username = input("What is your name: ")


class MyApp(App):
    def build(self):
        self.title = 'Leads Quote Generator'
        # Create the button and bind a callback function to its 'on_press' event
        btn = Button(text='Get Email', font_size=14)
        btn.bind(on_press=self.callback)
        return btn

    def callback(self, instance):
        print("Quote Loading")
        # The callback function is called when the button is pressed
        screenshot = pyautogui.screenshot()
        screenshot.save('screenshot\screenshot_1.png')
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        page_info = pytesseract.image_to_string(Image.open('screenshot\screenshot_1.png'))

        def extract_data(filename):
            # Simulate sample data instead of using a screenshot
            data = filename
            keywordz = ["WANTS", "SQFT", "BED", "BATH"]
            extracted_data = {}
            for keyword in keywordz:
                if keyword in data:
                    length = keyword.__len__()
                    num = ""
                    for k in range(8):
                        if data[data.index(keyword) + length + k + 1] != "\n":
                            num += data[data.index(keyword) + length + k + 1]
                    extracted_data[keyword] = num

            name = ["WANTS"]
            for keyword in name:
                if keyword in data:
                    first_name = ""
                    last_name = ""
                    k = 0
                    while data[data.index(keyword) + k - 1] == "\n" or data[data.index(keyword) + k - 1] == ",":
                        k -= 1

                    k -= 1
                    while data[data.index(keyword) + k - 1] != "\n" and data[data.index(keyword) + k - 1] != " ":
                        first_name = data[data.index(keyword) + k - 1] + first_name
                        k -= 1

                    k -= 1
                    while data[data.index(keyword) + k - 1] == "\n" or data[data.index(keyword) + k - 1] == ",":
                        k -= 1

                    # i -= 1
                    while data[data.index(keyword) + k - 1] != "\n" and data[data.index(keyword) + k - 1] != " ":
                        last_name = data[data.index(keyword) + k - 1] + last_name
                        k -= 1
                    extracted_data["last_name"] = last_name
                    extracted_data["first_name"] = first_name
            return extracted_data

        info = extract_data(page_info.upper())
        # print(page_info.upper())

        revised = []

        for i in info:
            word = info[i]
            revised_word = ""
            if i != "WANTS" and i != "last_name" and i != "first_name":
                for z in word:
                    before_revised_word = revised_word
                    # print(revised_word)
                    try:
                        revised_word += z
                        z = int(z)
                    except ValueError:
                        revised_word = before_revised_word
            elif i == "WANTS":
                finished = False
                for x in word:
                    if x != " " and not finished:
                        revised_word += x
                    else:
                        finished = True
            else:
                finished = False
                rep = 0
                for x in word:
                    if x != " " and not finished:
                        if rep == 0:
                            revised_word += x
                        else:
                            revised_word += x.lower()
                    else:
                        finished = True
                    rep += 1

            if i == "BATH":
                revised_word = int(revised_word)
                if revised_word >= 10:
                    revised_word = revised_word/10
                revised_word = str(revised_word)
            revised.append(revised_word)

        keywords = list(info)
        # print(keywords, revised)

        clean_type = "ONETIME"
        clean_sqft = 0
        clean_beds = 0
        clean_baths = 0
        clean_last_name = "there"
        clean_first_name = "there"

        for i in keywords:
            # print(i, revised[keywords.index(i)])
            if i == "WANTS":
                clean_type = revised[keywords.index(i)]
            if i == "SQFT":
                clean_sqft = revised[keywords.index(i)]
            if i == "BED":
                clean_beds = revised[keywords.index(i)]
            if i == "BATH":
                clean_baths = revised[keywords.index(i)]
            if i == "last_name":
                clean_last_name = revised[keywords.index(i)]
            if i == "first_name":
                clean_first_name = revised[keywords.index(i)]

        def calc_price(sqft, beds, baths, type_clean, name_first):
            elite = 250
            ongoing = 140
            # These are the base prices that are the minimum cost of cleans
            price_sqft = calc_sqft_price(int(sqft))
            # On the calculator on excelsheet, "NO TOUCH k9" is the same as "before price"
            before_price = float(baths) * 30 + float(beds) * 5 + price_sqft
            if type_clean == 0:
                elite = before_price * 2.9 * 1.1 * .81
            if type_clean == 1:
                elite = before_price * 2.9 * 1.1 * 1.15 * .81
            if type_clean == 2:
                ongoing = before_price * .9 * .95
            if type_clean == 3:
                ongoing = before_price * 1 * .95
            if type_clean == 4:
                ongoing = before_price * 1.33 * .95

            if type_clean == 2 or type_clean == 3 or type_clean == 4:
                elite = before_price * 2.5 * 1.103 * .65
                if ongoing < 140:
                    ongoing = 140
            if elite < 250:
                elite = 250
            title = get_title(clean_sqft, clean_beds, clean_baths, list_for_scripts, clean_last_name, clean_first_name)
            pyperclip.copy(title)
            time.sleep(0.4)
            main_info = get_quote(round(elite), round(ongoing), list_for_scripts, name_first)
            pyperclip.copy(main_info)
            print("Quote Complete")
            return elite, ongoing

        # This is all the different scripts
        def get_title(sqft, beds, baths, part_list, last, first):
            sqft = int(sqft)
            sqft = round(sqft/10)*10
            beds = int(beds)
            try:
                baths = int(baths)
            except ValueError:
                baths = float(baths)

            if beds <= 1 >= baths:
                scripts = [f"{last}, {first} - One Time Clean {sqft}, {beds} Bed, {baths} Bath",
                           f"{last}, {first} - Move Clean {sqft}, {beds} Bed, {baths} Bath",
                           f"{last}, {first} - Weekly Cleans {sqft}, {beds} Bed, {baths} Bath",
                           f"{last}, {first} - Biweekly Cleans {sqft}, {beds} Bed, {baths} Bath",
                           f"{last}, {first} - Monthly Cleans {sqft}, {beds} Bed, {baths} Bath"]
            elif beds > 1 < baths:
                scripts = [f"{last}, {first} - One Time Clean {sqft}, {beds} Beds, {baths} Baths",
                           f"{last}, {first} - Move Clean {sqft}, {beds} Beds, {baths} Baths",
                           f"{last}, {first} - Weekly Cleans {sqft}, {beds} Beds, {baths} Baths",
                           f"{last}, {first} - Biweekly Cleans {sqft}, {beds} Beds, {baths} Baths",
                           f"{last}, {first} - Monthly Cleans {sqft}, {beds} Beds, {baths} Baths"]
            elif beds > 1 >= baths:
                scripts = [f"{last}, {first} - One Time Clean {sqft}, {beds} Beds, {baths} Bath",
                           f"{last}, {first} - Move Clean {sqft}, {beds} Beds, {baths} Bath",
                           f"{last}, {first} - Weekly Cleans {sqft}, {beds} Beds, {baths} Bath",
                           f"{last}, {first} - Biweekly Cleans {sqft}, {beds} Beds, {baths} Bath",
                           f"{last}, {first} - Monthly Cleans {sqft}, {beds} Beds, {baths} Bath"]
            else:
                scripts = [f"{last}, {first} - One Time Clean {sqft}, {beds} Bed, {baths} Baths",
                           f"{last}, {first} - Move Clean {sqft}, {beds} Bed, {baths} Baths",
                           f"{last}, {first} - Weekly Cleans {sqft}, {beds} Bed, {baths} Baths",
                           f"{last}, {first} - Biweekly Cleans {sqft}, {beds} Bed, {baths} Baths",
                           f"{last}, {first} - Monthly Cleans {sqft}, {beds} Bed, {baths} Baths"]

            return scripts[part_list]

        def get_quote(initial, recuring, part_list, name="there"):
            scripts = [f"""Hi {name},

We're grateful for the opportunity to help with your cleaning needs!

Based on the info you provided and our March special, your one-time clean will be ${initial} (Includes washing all interior window panes within arms reach!)
•	        Would you like any extras like fridge, oven, window blind or track cleaning?
•	        Are there any other cleaning needs/notes you would like for me to add to our list?
Please let me know if you would like to get on the schedule and if you have any preferred days/times. Our schedule fills up quickly, but we still have a few spots open in March!

We look forward to cleaning for you!
{username}""", f"""Hi {name},

We're grateful for the opportunity to help with your cleaning needs!

Based on the info you provided and our March special, your moving clean will be ${initial} (Includes washing all interior window panes within arms reach!)
•	        Would you like any extras like fridge, oven, window blind or track cleaning?
•	        Are there any other cleaning needs/notes you would like for me to add to our list?
Please let me know if you would like to get on the schedule and if you have any preferred days/times. Our schedule fills up quickly, but we still have a few spots open in March!

We look forward to cleaning for you!
{username}""", f"""Hi {name}!

We're grateful for the opportunity to help with your cleaning needs!

Based on the info provided, and a special we are running for March, your initial reset clean will be ${initial} (this clean will be 2-3x as long and includes washing all interior window panes within arms reach) and weekly service is ${recuring}.

Please let me know if you would like to get on the schedule and if you have any preferred days/times. Our schedule fills up quickly (especially for the longer initial clean!), but we still have a few spots in March! What works best?

We look forward to cleaning for you!
{username}
""", f"""Hi {name}!

We're grateful for the opportunity to help with your cleaning needs!

Based on the info provided, and a special we are running for March, your initial reset clean will be ${initial} (this clean will be 2-3x as long and includes washing all interior window panes within arms reach) and biweekly service is ${recuring}.

Please let me know if you would like to get on the schedule and if you have any preferred days/times. Our schedule fills up quickly (especially for the longer initial clean!), but we still have a few spots in March! What works best?

We look forward to cleaning for you!
{username}
""", f"""Hi {name}!

We're grateful for the opportunity to help with your cleaning needs!

Based on the info provided, and a special we are running for March, your initial reset clean will be ${initial} (this clean will be 2-3x as long and includes washing all interior window panes within arms reach) and monthly service is ${recuring}.

Please let me know if you would like to get on the schedule and if you have any preferred days/times. Our schedule fills up quickly (especially for the longer initial clean!), but we still have a few spots in March! What works best?

We look forward to cleaning for you!
{username}
"""]

            return scripts[part_list]

        scripts_choose = ["ONETIME", "MOVE", "WEEKLY", "BIWEEKLY", "MONTHLY"]
        list_for_scripts = scripts_choose.index(clean_type)

        def calc_sqft_price(sqft):
            sqft_price = 70
            if sqft < 1000.01:
                sqft_price = 70
            elif sqft < 2000.01:
                sqft_price = 90
            elif sqft < 2601:
                sqft_price = 120
            elif sqft < 3500:
                sqft_price = 140
            elif sqft < 4200:
                sqft_price = 160
            elif sqft < 10500:
                sqft_price = sqft*.05
            return sqft_price

        calc_price(clean_sqft, clean_beds, clean_baths, list_for_scripts, clean_first_name)


if __name__ == "__main__":
    MyApp().run()
