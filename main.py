from scripts import get_title, get_quote, get_quote_manual, get_title_manual, get_quote_text
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
comp_mon = int(input("What monitor will you be using? "))

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

import mss
import mss.tools
import os


def get_screenshot(com_mon=1):
    with mss.mss() as sct:
        # Get information of monitor 2
        monitor_number = com_mon
        mon = sct.monitors[monitor_number]

        # The screen part to capture
        monitor = {
            "top": mon["top"],
            "left": mon["left"],
            "width": mon["width"],
            "height": mon["height"],
            "mon": monitor_number,
        }
        output = "screenshot_1.png".format(**monitor)

        # Determine the path to the "screenshot" folder
        path_to_screenshot_folder = os.path.join(os.path.dirname(__file__), "screenshot")

        # Create the "screenshot" folder if it doesn't exist
        os.makedirs(path_to_screenshot_folder, exist_ok=True)

        # Construct the full output path for the screenshot
        output_path = os.path.join(path_to_screenshot_folder, output)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save the screenshot to the specified path
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_path)

        # print("Screenshot saved to:", output_path)
        return output_path


class MyApp(App):
    def build(self):
        self.title = 'Leads Quote Generator'

        # Create the main layout
        main_layout = BoxLayout(orientation='vertical')

        # Create a layout for horizontal alignment of beds, baths, sqft
        input_layout = BoxLayout(orientation='horizontal', padding=0, spacing=0)

        # Add text input fields for user input
        self.type_input = TextInput(hint_text='Enter Clean Type', font_size=14)
        self.beds_input = TextInput(hint_text='Enter Beds', font_size=14)
        self.baths_input = TextInput(hint_text='Enter Baths', font_size=14)
        self.sqft_input = TextInput(hint_text='Enter Sqft', font_size=14)
        input_layout.add_widget(self.sqft_input)
        input_layout.add_widget(self.beds_input)
        input_layout.add_widget(self.baths_input)
        input_layout.add_widget(self.type_input)

        # Add the horizontal layout to the main layout
        main_layout.add_widget(input_layout)

        # Create a layout for vertical alignment of buttons
        button_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)

        # Create buttons with placeholders for callback functions

        def change_button_color(btn, pressed):
            if btn.background_color == [1, 0, 0, 1]:
                btn.background_color = (1, 1, 1, 1)
            else:
                btn.background_color = (1, 0, 0, 1)

        btn2 = Button(text='Manually Generate', font_size=14)
        btn2.bind(on_press=self.callback2)
        button_layout.add_widget(btn2)

        btn1 = Button(text='Get From Email', font_size=14)
        btn1.bind(on_press=lambda x: change_button_color(btn1, x))
        btn1.bind(on_press=self.callback1)
        button_layout.add_widget(btn1)

        # Add the vertical layout to the main layout
        main_layout.add_widget(button_layout)

        return main_layout

    def callback1(self, instance):
        print("Quote Loading")
        # The callback function is called when the button is pressed
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        # Using this as the screenshot function instead because it can do either monitors
        page_info = pytesseract.image_to_string(Image.open(get_screenshot(comp_mon)))

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
                    while data[data.index(keyword) + k - 1] == "\n" or data[data.index(keyword) + k - 1] == "," or data[data.index(keyword) + k - 1] == " ":
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



            text_info = get_quote_text(round(elite), round(ongoing), list_for_scripts, name_first, username, clean_sqft,
                                       clean_beds, clean_baths)
            pyperclip.copy(text_info)
            time.sleep(0.4)
            title = get_title(clean_sqft, clean_beds, clean_baths, list_for_scripts, clean_last_name, clean_first_name)
            pyperclip.copy(title)
            time.sleep(0.4)
            main_info = get_quote(round(elite), round(ongoing), list_for_scripts, name_first, username)
            pyperclip.copy(main_info)
            print("Quote Complete")
            return elite, ongoing

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

    def callback2(self, instance):
        print("Quote Loading")

        # clean_type = "ONETIME"
        clean_sqft = 0
        clean_beds = 0
        clean_baths = 0
        clean_first_name = "there"

        clean_type = self.type_input.text
        clean_sqft = self.sqft_input.text
        clean_beds = self.beds_input.text
        clean_baths = self.baths_input.text

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

            text_info = get_quote_text(round(elite), round(ongoing), list_for_scripts, name_first, username, clean_sqft,
                                       clean_beds, clean_baths)
            pyperclip.copy(text_info)
            time.sleep(0.4)
            title = get_title_manual(clean_sqft, clean_beds, clean_baths, list_for_scripts)
            pyperclip.copy(title)
            time.sleep(0.4)
            main_info = get_quote_manual(round(elite), round(ongoing), list_for_scripts, name_first, username)
            pyperclip.copy(main_info)
            print("Quote Complete")
            return elite, ongoing

        scripts_choose = ["ONETIME", "MOVE", "WEEKLY", "BIWEEKLY", "MONTHLY"]
        print(clean_type)
        list_for_scripts = scripts_choose.index(clean_type.upper())

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
                sqft_price = sqft * .05
            return sqft_price

        calc_price(clean_sqft, clean_beds, clean_baths, list_for_scripts, clean_first_name)


if __name__ == "__main__":
    MyApp().run()
