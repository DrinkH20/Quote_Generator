from scripts import get_title, get_quote, get_title_manual, get_quote_text, failed
from PIL import Image
import pytesseract
import pyperclip
import time
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', '220')
Config.set('graphics', 'height', '150')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'left', 20)
Config.set('graphics', 'top', 50)
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import mss
import mss.tools
import os

from datetime import date

today = date.today()

months_list = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
month = months_list[today.month-1]


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


class MyLayout(Screen):
    def change_button_color(self, btn, error_color=False):
        if btn == "1":
            if self.ids.button_1.background_color == [1, 0, 0, 1]:
                self.ids.button_1.background_color = (1, 1, 1, 1)
            else:
                self.ids.button_1.background_color = (1, 0, 0, 1)
            if error_color:
                self.ids.button_1.background_color = (1, 0, 1, 1)

        elif btn == "2":
            if self.ids.button_2.background_color == [1, 0, 0, 1]:
                self.ids.button_2.background_color = (1, 1, 1, 1)
            else:
                self.ids.button_2.background_color = (1, 0, 0, 1)
            if error_color:
                self.ids.button_2.background_color = (1, 0, 1, 1)

    def callback1(self, instance):
        try:
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
                try:
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

                except ValueError and UnboundLocalError and IndexError and UnboundLocalError:
                    print("Error Loading Quote")
                    self.change_button_color("2", True)
                    body_paragraph = failed(month, username)
                    pyperclip.copy(body_paragraph)

                return extracted_data

            info = extract_data(page_info.upper())

            # print(page_info)

            revised = []

            if len(info) == 6:
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
                    try:
                        if i == "BATH":
                            revised_word = int(revised_word)
                            if revised_word >= 10:
                                revised_word = revised_word/10
                            revised_word = str(revised_word)
                    except ValueError:
                        print("Did not collect all info")
                        self.change_button_color("2", True)
                        body_paragraph = failed(month, username)
                        pyperclip.copy(body_paragraph)

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
            else:
                print("Did not collect all info")
                self.change_button_color("2", True)
                body_paragraph = failed(month, username)
                pyperclip.copy(body_paragraph)

            def calc_price(sqft, beds, baths, type_clean, name_first):
                elite = 250
                ongoing = 140
                try:
                    # These are the base prices that are the minimum cost of cleans
                    try:
                        price_sqft = calc_sqft_price(int(sqft))
                        before_price = float(baths) * 30 + float(beds) * 5 + price_sqft
                    except ValueError:
                        print("Error Loading Quote")
                        self.change_button_color("2", True)
                        body_paragraph = failed(month, username)
                        pyperclip.copy(body_paragraph)

                    # ["ONETIME", "MOVE", "WEEKLY", "BIWEEKLY", "MONTHLY"]
                    if type_clean == 0:
                        elite = before_price * 2.9 * 1.1 * .95
                    if type_clean == 1:
                        elite = before_price * 2.9 * 1.1 * 1.15 * .95
                    if type_clean == 2:
                        ongoing = before_price * .9 * 1.01
                    if type_clean == 3:
                        ongoing = before_price * 1 * 1.01
                    if type_clean == 4:
                        ongoing = before_price * 1.33 * 1.07

                    if type_clean == 2 or type_clean == 3 or type_clean == 4:
                        elite = before_price * 2.5 * 1.1 * .65
                        if ongoing < 140:
                            ongoing = 140
                    if elite < 250:
                        elite = 250

                    text_info = get_quote_text(month, round(elite), round(ongoing), list_for_scripts, name_first, username, clean_sqft,
                                               clean_beds, clean_baths)
                    pyperclip.copy(text_info)
                    time.sleep(0.4)
                    title = get_title(clean_sqft, clean_beds, clean_baths, list_for_scripts, clean_last_name, clean_first_name)
                    pyperclip.copy(title)
                    time.sleep(0.4)
                    main_info = get_quote(month, round(elite), round(ongoing), list_for_scripts, name_first, username)
                    pyperclip.copy(main_info)

                    # On the calculator on excelsheet, "NO TOUCH k9" is the same as "before price"

                    print("Quote Complete")
                except ValueError and UnboundLocalError and IndexError and UnboundLocalError:
                    print("Error Loading Quote")
                    self.change_button_color("2", True)
                    body_paragraph = failed(month, username)
                    pyperclip.copy(body_paragraph)

                return elite, ongoing

            scripts_choose = ["ONETIME", "MOVE", "WEEKLY", "BIWEEKLY", "MONTHLY"]

            try:
                list_for_scripts = scripts_choose.index(clean_type)
            except ValueError:
                print("Error Loading Quote")
                self.change_button_color("2", True)
                body_paragraph = failed(month, username)
                pyperclip.copy(body_paragraph)

            def calc_sqft_price(sqft):
                sqft_price = 70
                try:
                    if sqft < 1000:
                        sqft_price = 70
                    elif sqft < 2000.01:
                        sqft_price = 90
                    elif sqft < 2701:
                        sqft_price = 120
                    elif sqft < 3500.01:
                        sqft_price = 140
                    elif sqft < 4200:
                        sqft_price = 160
                    elif sqft < 10500:
                        sqft_price = sqft*.05
                except ValueError and UnboundLocalError and IndexError and UnboundLocalError:
                    print("Error Loading Quote")
                    self.change_button_color("2", True)
                    body_paragraph = failed(month, username)
                    pyperclip.copy(body_paragraph)
                return sqft_price

            calc_price(clean_sqft, clean_beds, clean_baths, list_for_scripts, clean_first_name)
        except ValueError and UnboundLocalError and IndexError and UnboundLocalError:
            print("Error Loading Quote")
            self.change_button_color("2", True)
            body_paragraph = failed(month, username)
            pyperclip.copy(body_paragraph)

    def callback2(self, instance):
        try:
            print("Quote Loading")

            # clean_type = "ONETIME"
            clean_sqft = 0
            clean_beds = 0
            clean_baths = 0
            clean_first_name = "there"
            clean_type = self.ids.type_input.text
            clean_sqft = self.ids.sqft_input.text
            clean_beds = self.ids.beds_input.text
            clean_baths = self.ids.baths_input.text

            clean_last_name = self.ids.last_name_input.text

            names = False
            if clean_last_name != "":
                clean_first_name = self.ids.first_name_input.text
                names = True

            def calc_price(sqft, beds, baths, type_clean, name_first, name_last):
                elite = 250
                ongoing = 140
                try:
                    # These are the base prices that are the minimum cost of cleans
                    try:
                        price_sqft = calc_sqft_price(int(sqft))
                    except ValueError:
                        print("Error Loading Quote")
                        self.change_button_color("2", True)
                        body_paragraph = failed(month, username)
                        pyperclip.copy(body_paragraph)
                    # On the calculator on excelsheet, "NO TOUCH k9" is the same as "before price"
                    before_price = float(baths) * 30 + float(beds) * 5 + price_sqft

                    # ["ONETIME", "MOVE", "WEEKLY", "BIWEEKLY", "MONTHLY"]
                    print(before_price)
                    if type_clean == 0:
                        elite = before_price * 2.9 * 1.1 * .95
                    if type_clean == 1:
                        elite = before_price * 2.9 * 1.1 * 1.15 * 1
                    if type_clean == 2:
                        ongoing = before_price * .9 * 1.01
                    if type_clean == 3:
                        ongoing = before_price * 1 * 1.01
                    if type_clean == 4:
                        ongoing = before_price * 1.33 * 1.05

                    if type_clean == 2 or type_clean == 3 or type_clean == 4:
                        elite = before_price * 2.5 * 1.103 * .65
                        if ongoing < 140:
                            ongoing = 140
                    if elite < 250:
                        elite = 250

                    text_info = get_quote_text(month, round(elite), round(ongoing), list_for_scripts, name_first, username, clean_sqft,
                                               clean_beds, clean_baths)
                    pyperclip.copy(text_info)
                    time.sleep(0.4)
                    if names:
                        title = get_title(clean_sqft, clean_beds, clean_baths, list_for_scripts, name_last, name_first)
                        pyperclip.copy(title)
                        time.sleep(0.4)
                        main_info = get_quote(month, round(elite), round(ongoing), list_for_scripts, name_first, username)
                    else:
                        title = get_title_manual(clean_sqft, clean_beds, clean_baths, list_for_scripts)
                        pyperclip.copy(title)
                        time.sleep(0.4)
                        main_info = get_quote(month, round(elite), round(ongoing), list_for_scripts, name_first, username)
                    pyperclip.copy(main_info)
                    print("Quote Complete")

                except ValueError and UnboundLocalError and IndexError and UnboundLocalError:
                    print("Error Loading Quote")
                    self.change_button_color("2", True)
                    body_paragraph = failed(month, username)
                    pyperclip.copy(body_paragraph)
                return elite, ongoing

            scripts_choose = ["ONETIME", "MOVE", "WEEKLY", "BIWEEKLY", "MONTHLY"]

            try:
                if clean_type != "":
                    list_for_scripts = scripts_choose.index(clean_type.upper())

            except ValueError and UnboundLocalError and IndexError and UnboundLocalError:
                print("Error Loading Quote")
                self.change_button_color("2", True)
                body_paragraph = failed(month, username)
                pyperclip.copy(body_paragraph)

            def calc_sqft_price(sqft):
                sqft_price = 70
                try:
                    if sqft < 1000.01:
                        sqft_price = 70
                    elif sqft < 2000.01:
                        sqft_price = 90
                    elif sqft < 2701:
                        sqft_price = 120
                    elif sqft < 3500.01:
                        sqft_price = 140
                    elif sqft < 4200:
                        sqft_price = 160
                    elif sqft < 10500:
                        sqft_price = sqft * .05

                except ValueError and UnboundLocalError and IndexError and UnboundLocalError:
                    print("Error Loading Quote")
                    self.change_button_color("2", True)
                    body_paragraph = failed(month, username)
                    pyperclip.copy(body_paragraph)

                return sqft_price

            calc_price(clean_sqft, clean_beds, clean_baths, list_for_scripts, clean_first_name, clean_last_name)
        except ValueError and UnboundLocalError and IndexError and UnboundLocalError:
            print("Error Loading Quote")
            self.change_button_color("2", True)
            body_paragraph = failed(month, username)
            pyperclip.copy(body_paragraph)


class SettingWindow(Screen):
    def update(self, btn):
        global username
        global comp_mon
        if self.ids.username_input.text != "":
            username = self.ids.username_input.text
        else:
            print("No Name Entered")
        try:
            comp_mon = self.ids.screen_input.text
            comp_mon = int(comp_mon)
        except ValueError:
            print("No Monitor Entered")
        print("Updated!")
    pass


class WindowManage(ScreenManager):
    pass


kv = Builder.load_file('my.kv')
username = input("What is your name: ")
comp_mon = int(input("What monitor will you be using? "))


class MyApp(App):
    def build(self):
        self.title = 'Leads Quote Generator'
        return kv


if __name__ == "__main__":
    MyApp().run()
