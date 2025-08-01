from scripts import get_title, get_quote, get_title_manual, get_quote_text, failed, out_of_service_area, get_quote_text_dfw, get_quote_dfw
from PIL import Image
from server_price_connect import update_servers
import pytesseract
import pyperclip
import time
from kivy.config import Config
Config.set('graphics', 'width', '220')
Config.set('graphics', 'height', '150')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 20)
Config.set('graphics', 'top', 50)
Config.set('graphics', 'resizable', 1)

# Now import Kivy modules
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ListProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

import mss
import mss.tools
import os

from datetime import date

if os.path.exists("token.pickle"):
    os.remove("token.pickle")
    print("token.pickle has been deleted")
else:
    print("token.pickle does not exist")


today = date.today()

months_list = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
month = months_list[today.month-1]

market = "PDX"

# Discounts:
moving_discount = .05
onetime_discount = .05

# Updates from the estimator on googlesheets
# These are all the factors that need to be used to multiply the base price by to get the correct price to leads
ot, initial, move, monthly, biweekly, weekly = 1, 1, 1, 1, 1, 1
texas_factors = []

def get_prices_googlesheets(mark):
    global ot, initial, move, monthly, biweekly, weekly, texas_factors
    factors, texas_factors = update_servers(mark)
    set_ot, set_initial, set_move, set_monthly, set_biweekly, set_weekly = map(float, factors)
    # print(texas_factors)
    if (ot, initial, move, monthly, biweekly, weekly) == (set_ot, set_initial, set_move, set_monthly, set_biweekly, set_weekly):
        print("No change needed")
    else:
        ot, initial, move, monthly, biweekly, weekly = set_ot, set_initial, set_move, set_monthly, set_biweekly, set_weekly
        print("Prices successfully updated!")
    # print(ot, initial, move, monthly, biweekly, weekly)


get_prices_googlesheets(market)


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
    title_text = StringProperty("Get PDX Quotes")
    title_color = ListProperty([0.2, 0.2, 0.9, 1])  # Blueish

    def update_last_focused(self, instance, value):
        if value:  # Only when it's gaining focus
            self.last_focused = instance

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self.on_key_down)
        self.focus_chain = []  # We'll fill this in `on_kv_post`
        for widget in self.focus_chain:
            widget.bind(focus=self.update_last_focused)
        self.last_focused = None

    def on_kv_post(self, base_widget):
        # Define focus order once widgets are loaded
        self.focus_chain = [
            self.ids.first_name_input,
            self.ids.last_name_input,
            self.ids.sqft_input,
            self.ids.beds_input,
            self.ids.baths_input
        ]

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 9:  # Tab
            shift_pressed = "shift" in modifiers

            if self.last_focused and self.last_focused in self.focus_chain:
                index = self.focus_chain.index(self.last_focused)

                if shift_pressed:
                    next_index = (index - 1) % len(self.focus_chain)
                else:
                    next_index = (index + 1) % len(self.focus_chain)

                self.focus_chain[next_index].focus = True
                return True  # Prevent default tab behavior
        return False

    def change_button_type(self, change="False"):
        self.ids.cleantype.text = change

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
                elite = 200
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
                    dfw_type_clean = type_clean
                    if type_clean == 0:
                        elite = before_price * ot
                    if type_clean == 1:
                        elite = before_price * move
                    if type_clean == 2:
                        ongoing = before_price * weekly
                    if type_clean == 3:
                        ongoing = before_price * biweekly
                    if type_clean == 4:
                        ongoing = before_price * monthly
                    if dfw_type_clean >= 2:
                        dfw_type_clean += 1

                    # Order of cleanings is switched on the estimator to go OT initial move monthly biweekly week. So i swap the weekly and monthly numbers
                    if dfw_type_clean == 3:
                        dfw_type_clean = 5
                    elif dfw_type_clean == 5:
                        dfw_type_clean = 3

                    if market == "DFW":
                        elite = elite * texas_factors[dfw_type_clean]

                    if type_clean == 2 or type_clean == 3 or type_clean == 4:
                        elite = before_price * initial
                        if ongoing < 140:
                            ongoing = 140
                    if market == "DFW":
                        ongoing = ongoing * texas_factors[dfw_type_clean]
                    if elite < 200:
                        elite = 200

                    if market == "PDX":
                        text_info = get_quote_text(month, round(elite), round(ongoing), list_for_scripts, name_first, username, clean_sqft,
                                                   clean_beds, clean_baths)
                    elif market == "DFW":
                        text_info = get_quote_text_dfw(month, round(elite), round(ongoing), list_for_scripts, name_first,
                                                   username, clean_sqft,
                                                   clean_beds, clean_baths)
                    pyperclip.copy(f"Lead {name_first} {clean_last_name}")
                    time.sleep(0.4)
                    pyperclip.copy(text_info)
                    time.sleep(0.4)
                    title = get_title(clean_sqft, clean_beds, clean_baths, list_for_scripts, clean_last_name, clean_first_name)
                    pyperclip.copy(title)
                    time.sleep(0.4)
                    if market == "PDX":
                        main_info = get_quote(month, round(elite), round(ongoing), list_for_scripts, name_first,
                                              username)
                    elif market == "DFW":
                        main_info = get_quote_dfw(month, round(elite), round(ongoing), list_for_scripts, name_first,
                                              username)
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
                        sqft_price = 250
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

            def calc_price(name_first, name_last, sqft, beds, baths, type_clean):
                elite = 200
                ongoing = 140
                try:
                    print(type(float(sqft)), type(float(beds)), type(float(baths)))
                except ValueError:
                    return "Failed"

                try:
                    # These are the base prices that are the minimum cost of cleans
                    try:
                        price_sqft = calc_sqft_price(int(sqft))
                    except ValueError:
                        print("Error Loading Quote")
                        self.change_button_color("1", True)
                        body_paragraph = failed(month, username)
                        pyperclip.copy(body_paragraph)

                    if baths != '':
                        # On the calculator on excelsheet, "NO TOUCH k9" is the same as "before price"
                        before_price = float(baths) * 30 + float(beds) * 5 + price_sqft

                        # ["ONETIME", "MOVE", "WEEKLY", "BIWEEKLY", "MONTHLY"]
                        dfw_type_clean = type_clean
                        if type_clean == 0:
                            elite = before_price * ot
                        if type_clean == 1:
                            elite = before_price * move
                        if type_clean == 2:
                            ongoing = before_price * weekly
                        if type_clean == 3:
                            ongoing = before_price * biweekly
                        if type_clean == 4:
                            ongoing = before_price * monthly
                        if dfw_type_clean >= 1:
                            dfw_type_clean += 1

                        # Order of cleanings is switched on the estimator to go OT initial move monthly biweekly week. So i swap the weekly and monthly numbers
                        if dfw_type_clean == 3:
                            dfw_type_clean = 5
                        elif dfw_type_clean == 5:
                            dfw_type_clean = 3

                        if market == "DFW":
                            elite = elite * texas_factors[dfw_type_clean]

                        if type_clean == 2 or type_clean == 3 or type_clean == 4:
                            elite = before_price * initial
                            if ongoing < 140:
                                ongoing = 140
                        if market == "DFW":
                            ongoing = ongoing * texas_factors[dfw_type_clean]
                        if elite < 200:
                            elite = 200

                    pyperclip.copy(f"Lead {name_first} {name_last}")
                    time.sleep(0.4)
                    if market == "PDX":
                        text_info = get_quote_text(month, round(elite), round(ongoing), list_for_scripts, name_first,
                                                   username, clean_sqft,
                                                   clean_beds, clean_baths)
                    elif market == "DFW":
                        text_info = get_quote_text_dfw(month, round(elite), round(ongoing), list_for_scripts,
                                                       name_first,
                                                       username, clean_sqft,
                                                       clean_beds, clean_baths)
                    pyperclip.copy(text_info)
                    time.sleep(0.4)

                    if names:
                        title = get_title(clean_sqft, clean_beds, clean_baths, list_for_scripts, name_last, name_first)
                        # Error handling
                        if title == "Failed":
                            print("Error Loading Quotes")
                            self.change_button_color("1", True)
                        else:
                            pyperclip.copy(title)
                            time.sleep(0.4)
                            if market == "PDX":
                                main_info = get_quote(month, round(elite), round(ongoing), list_for_scripts, name_first,
                                                      username)
                            elif market == "DFW":
                                main_info = get_quote_dfw(month, round(elite), round(ongoing), list_for_scripts,
                                                          name_first,
                                                          username)
                    else:
                        title = get_title_manual(clean_sqft, clean_beds, clean_baths, list_for_scripts)
                        pyperclip.copy(title)
                        time.sleep(0.4)
                        if market == "PDX":
                            main_info = get_quote(month, round(elite), round(ongoing), list_for_scripts, name_first,
                                                  username)
                        elif market == "DFW":
                            main_info = get_quote_dfw(month, round(elite), round(ongoing), list_for_scripts, name_first,
                                                      username)
                    pyperclip.copy(main_info)
                    print("Quote Complete")

                except ValueError and UnboundLocalError and IndexError and UnboundLocalError:
                    print("Error Loading Quote")
                    self.change_button_color("1", True)
                    body_paragraph = failed(month, username)
                    pyperclip.copy(body_paragraph)
                return elite, ongoing

            scripts_choose = ["ONETIME", "MOVE", "WEEKLY", "BIWEEKLY", "MONTHLY", "FAR"]

            try:
                if clean_type != "":
                    list_for_scripts = scripts_choose.index(clean_type.upper())

            except ValueError and UnboundLocalError and IndexError and UnboundLocalError:
                print("Error Loading Quote")
                self.change_button_color("1", True)
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
                        sqft_price = 250

                except ValueError and UnboundLocalError and IndexError and UnboundLocalError:
                    print("Error Loading Quote")
                    self.change_button_color("1", True)
                    body_paragraph = failed(month, username)
                    pyperclip.copy(body_paragraph)

                return sqft_price

            if calc_price(clean_first_name, clean_last_name, clean_sqft, clean_beds, clean_baths, list_for_scripts) == "Failed":
                print("Error Loading Quotes")
                self.change_button_color("1", True)
                if list_for_scripts != 5:
                    body_paragraph = failed(month, username)
                else:
                    title = get_title(clean_sqft, clean_beds, clean_baths, list_for_scripts, clean_last_name, clean_first_name)
                    pyperclip.copy(title)
                    time.sleep(0.4)
                    body_paragraph = out_of_service_area(username)
                pyperclip.copy(body_paragraph)
        except ValueError and UnboundLocalError and IndexError and UnboundLocalError:
            print("Error Loading Quote")
            self.change_button_color("1", True)
            body_paragraph = failed(month, username)
            pyperclip.copy(body_paragraph)


class CleanType(Screen):
    pass


class SettingWindow(Screen):
    if market == "PDX":
        bg_color = ListProperty([0, 0, 1, 1])
    else:
        bg_color = ListProperty([1, 0, 0, 1])
    title_text = StringProperty("Get PDX Quotes")
    title_color = ListProperty([0.2, 0.2, 0.9, 1])  # Blueish

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

    def update_price_pdx(self, *args):
        global market
        market = "PDX"

        # Access MyLayout screen via screen manager
        main_screen = self.manager.get_screen("main")


        main_screen.title_text = "Get PDX Quotes"
        self.bg_color = [0, 0, 1, 1]  # ✅ not ListProperty(...)
        main_screen.title_color = [0.2, 0.2, 0.9, 1]

        get_prices_googlesheets(market)
        print("Updated!")

    def update_price_dfw(self, *args):
        global market
        market = "DFW"

        # Access MyLayout screen via screen manager
        main_screen = self.manager.get_screen("main")

        main_screen.title_text = "Get DFW Quotes"
        main_screen.title_color = [0.9, 0.2, 0.2, 1]
        self.bg_color = [1, 0, 0, 1]  # ✅ just assign a new value

        get_prices_googlesheets(market)
        print("Updated!")



class WindowManage(ScreenManager):
    pass


kv = Builder.load_file('my.kv')
username = input("What is your name: ")
comp_mon = int(input("What monitor will you be using? "))


class MyApp(App):
    def change_screen_and_update(self, screen_name, update_value):
        # Change the screen
        self.root.current = screen_name
        # Access the current screen's button and change the text
        screen = self.root.get_screen(screen_name)
        screen.ids.type_input.text = update_value

    def build(self):
        self.title = 'Leads Quote Generator'
        return kv


if __name__ == "__main__":
    MyApp().run()
