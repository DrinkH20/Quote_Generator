from gspread_pandas import Spread, Client
import re
import numpy as np


def update_servers():
    # Initialize the client and authenticate
    client = Client()

    # Access your Google Sheet by URL
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1VHiCVG3sYEwoeBHVkWruhEC5n2q5AL3K4SJzpYbj5XA/edit?gid=0#gid=0'
    spread = Spread(spreadsheet_url, client=client)

    # Get the gspread client from the spread object
    gsheet = spread.client.open_by_url(spreadsheet_url)

    # Access the specific sheet by name
    sheet = gsheet.worksheet('Estimator')

    # Access the formula in cell I20 (row 20, column 9) with the formula option
    formula = []
    cell = sheet.acell('I20', value_render_option='FORMULA')
    formula.append(cell.value)
    cell = sheet.acell('I22', value_render_option='FORMULA')
    formula.append(cell.value)
    cell = sheet.acell('I24', value_render_option='FORMULA')
    formula.append(cell.value)
    cell = sheet.acell('D26', value_render_option='FORMULA')
    formula.append(cell.value)
    cell = sheet.acell('D28', value_render_option='FORMULA')
    formula.append(cell.value)
    cell = sheet.acell('D30', value_render_option='FORMULA')
    formula.append(cell.value)

    # Regular expression to find all floats in the formula
    all_floats = []
    for i in formula:
        split_point = i.find('+')
        first_half = i[:split_point]
        numbers = re.findall(r'\d+\.\d+|\d+', first_half)
        numbers.pop(0)
        extracted_numbers = [float(num) if '.' in num else int(num) for num in numbers]
        all_floats.append(extracted_numbers)

    calc_factors = []
    # Multiply all the numbers in each sublist
    results = [np.prod(sublist) for sublist in all_floats]

    # Print the results
    for i, result in enumerate(results, start=1):
        calc_factors.append(f"{result:.5f}")
    return calc_factors
