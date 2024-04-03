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
        scripts = [f"{last}, {first} - One Time Clean {sqft} sqft, {beds} Bed, {baths} Bath",
                   f"{last}, {first} - Move Clean {sqft} sqft, {beds} Bed, {baths} Bath",
                   f"{last}, {first} - Weekly Cleans {sqft} sqft, {beds} Bed, {baths} Bath",
                   f"{last}, {first} - Biweekly Cleans {sqft} sqft, {beds} Bed, {baths} Bath",
                   f"{last}, {first} - Monthly Cleans {sqft} sqft, {beds} Bed, {baths} Bath"]
    elif beds > 1 < baths:
        scripts = [f"{last}, {first} - One Time Clean {sqft} sqft, {beds} Beds, {baths} Baths",
                   f"{last}, {first} - Move Clean {sqft} sqft, {beds} Beds, {baths} Baths",
                   f"{last}, {first} - Weekly Cleans {sqft} sqft, {beds} Beds, {baths} Baths",
                   f"{last}, {first} - Biweekly Cleans {sqft} sqft, {beds} Beds, {baths} Baths",
                   f"{last}, {first} - Monthly Cleans {sqft} sqft, {beds} Beds, {baths} Baths"]
    elif beds > 1 >= baths:
        scripts = [f"{last}, {first} - One Time Clean {sqft} sqft, {beds} Beds, {baths} Bath",
                   f"{last}, {first} - Move Clean {sqft} sqft, {beds} Beds, {baths} Bath",
                   f"{last}, {first} - Weekly Cleans {sqft} sqft, {beds} Beds, {baths} Bath",
                   f"{last}, {first} - Biweekly Cleans {sqft} sqft, {beds} Beds, {baths} Bath",
                   f"{last}, {first} - Monthly Cleans {sqft} sqft, {beds} Beds, {baths} Bath"]
    else:
        scripts = [f"{last}, {first} - One Time Clean {sqft} sqft, {beds} Bed, {baths} Baths",
                   f"{last}, {first} - Move Clean {sqft} sqft, {beds} Bed, {baths} Baths",
                   f"{last}, {first} - Weekly Cleans {sqft} sqft, {beds} Bed, {baths} Baths",
                   f"{last}, {first} - Biweekly Cleans {sqft} sqft, {beds} Bed, {baths} Baths",
                   f"{last}, {first} - Monthly Cleans {sqft} sqft, {beds} Bed, {baths} Baths"]

    return scripts[part_list]


def get_quote(initial, recuring, part_list, name="there", username=""):
    scripts = [f"""Hi {name},

We're grateful for the opportunity to help with your cleaning needs!

Based on the info you provided and our April special, your one-time clean will be ${initial} (Includes washing all interior window panes within arms reach!)
•	        Would you like any extras like fridge, oven, window blind or track cleaning?
•	        Are there any other cleaning needs/notes you would like for me to add to our list?
Please let me know if you would like to get on the schedule and if you have any preferred days/times. Our schedule fills up quickly, but we still have a few spots open in April!

We look forward to cleaning for you!
{username}""", f"""Hi {name},

We're grateful for the opportunity to help with your cleaning needs!

Based on the info you provided and our April special, your moving clean will be ${initial} (Includes washing all interior window panes within arms reach!)
•	        Would you like any extras like fridge, oven, window blind or track cleaning?
•	        Are there any other cleaning needs/notes you would like for me to add to our list?
Please let me know if you would like to get on the schedule and if you have any preferred days/times. Our schedule fills up quickly, but we still have a few spots open in April!

We look forward to cleaning for you!
{username}""", f"""Hi {name}!

We're grateful for the opportunity to help with your cleaning needs!

Based on the info provided, and a special we are running for April, your initial reset clean will be ${initial} (this clean will be 2-3x as long and includes washing all interior window panes within arms reach) and weekly service is ${recuring}.

Please let me know if you would like to get on the schedule and if you have any preferred days/times. Our schedule fills up quickly (especially for the longer initial clean!), but we still have a few spots in April! What works best?

We look forward to cleaning for you!
{username}
""", f"""Hi {name}!

We're grateful for the opportunity to help with your cleaning needs!

Based on the info provided, and a special we are running for April, your initial reset clean will be ${initial} (this clean will be 2-3x as long and includes washing all interior window panes within arms reach) and biweekly service is ${recuring}.

Please let me know if you would like to get on the schedule and if you have any preferred days/times. Our schedule fills up quickly (especially for the longer initial clean!), but we still have a few spots in April! What works best?

We look forward to cleaning for you!
{username}
""", f"""Hi {name}!

We're grateful for the opportunity to help with your cleaning needs!

Based on the info provided, and a special we are running for April, your initial reset clean will be ${initial} (this clean will be 2-3x as long and includes washing all interior window panes within arms reach) and monthly service is ${recuring}.

Please let me know if you would like to get on the schedule and if you have any preferred days/times. Our schedule fills up quickly (especially for the longer initial clean!), but we still have a few spots in April! What works best?

We look forward to cleaning for you!
{username}
"""]
    return scripts[part_list]


def get_title_manual(sqft, beds, baths, part_list):
    sqft = int(sqft)
    sqft = round(sqft / 10) * 10
    beds = int(beds)
    try:
        baths = int(baths)
    except ValueError:
        baths = float(baths)

    if beds <= 1 >= baths:
        scripts = [f"One Time Clean {sqft} sqft, {beds} Bed, {baths} Bath",
                   f"Move Clean {sqft} sqft, {beds} Bed, {baths} Bath",
                   f"Weekly Cleans {sqft} sqft, {beds} Bed, {baths} Bath",
                   f"Biweekly Cleans {sqft} sqft, {beds} Bed, {baths} Bath",
                   f"Monthly Cleans {sqft} sqft, {beds} Bed, {baths} Bath"]
    elif beds > 1 < baths:
        scripts = [f"One Time Clean {sqft} sqft, {beds} Beds, {baths} Baths",
                   f"Move Clean {sqft} sqft, {beds} Beds, {baths} Baths",
                   f"Weekly Cleans {sqft} sqft, {beds} Beds, {baths} Baths",
                   f"Biweekly Cleans {sqft} sqft, {beds} Beds, {baths} Baths",
                   f"Monthly Cleans {sqft} sqft, {beds} Beds, {baths} Baths"]
    elif beds > 1 >= baths:
        scripts = [f"One Time Clean {sqft} sqft, {beds} Beds, {baths} Bath",
                   f"Move Clean {sqft} sqft, {beds} Beds, {baths} Bath",
                   f"Weekly Cleans {sqft} sqft, {beds} Beds, {baths} Bath",
                   f"Biweekly Cleans {sqft} sqft, {beds} Beds, {baths} Bath",
                   f"Monthly Cleans {sqft} sqft, {beds} Beds, {baths} Bath"]
    else:
        scripts = [f"One Time Clean {sqft} sqft, {beds} Bed, {baths} Baths",
                   f"Move Clean {sqft} sqft, {beds} Bed, {baths} Baths",
                   f"Weekly Cleans {sqft} sqft, {beds} Bed, {baths} Baths",
                   f"Biweekly Cleans {sqft} sqft, {beds} Bed, {baths} Baths",
                   f"Monthly Cleans {sqft} sqft, {beds} Bed, {baths} Baths"]

    return scripts[part_list]


# def get_quote_manual(initial, recuring, part_list, name="there", username=""):
#     scripts = [f"""Hi {name},
#
# We're grateful for the opportunity to help with your cleaning needs!
#
# Based on the info you provided and our April special, your one-time clean will be ${initial} (Includes washing all interior window panes within arms reach!)
# •	        Would you like any extras like fridge, oven, window blind or track cleaning?
# •	        Are there any other cleaning needs/notes you would like for me to add to our list?
# Please let me know if you would like to get on the schedule and if you have any preferred days/times. Our schedule fills up quickly, but we still have a few spots open in April!
#
# We look forward to cleaning for you!
# {username}""", f"""Hi {name},
#
# We're grateful for the opportunity to help with your cleaning needs!
#
# Based on the info you provided and our April special, your moving clean will be ${initial} (Includes washing all interior window panes within arms reach!)
# •	        Would you like any extras like fridge, oven, window blind or track cleaning?
# •	        Are there any other cleaning needs/notes you would like for me to add to our list?
# Please let me know if you would like to get on the schedule and if you have any preferred days/times. Our schedule fills up quickly, but we still have a few spots open in April!
#
# We look forward to cleaning for you!
# {username}""", f"""Hi {name}!
#
# We're grateful for the opportunity to help with your cleaning needs!
#
# Based on the info provided, and a special we are running for April, your initial reset clean will be ${initial} (this clean will be 2-3x as long and includes washing all interior window panes within arms reach) and weekly service is ${recuring}.
#
# Please let me know if you would like to get on the schedule and if you have any preferred days/times. Our schedule fills up quickly (especially for the longer initial clean!), but we still have a few spots in April! What works best?
#
# We look forward to cleaning for you!
# {username}
# """, f"""Hi {name}!
#
# We're grateful for the opportunity to help with your cleaning needs!
#
# Based on the info provided, and a special we are running for April, your initial reset clean will be ${initial} (this clean will be 2-3x as long and includes washing all interior window panes within arms reach) and biweekly service is ${recuring}.
#
# Please let me know if you would like to get on the schedule and if you have any preferred days/times. Our schedule fills up quickly (especially for the longer initial clean!), but we still have a few spots in April! What works best?
#
# We look forward to cleaning for you!
# {username}
# """, f"""Hi {name}!
#
# We're grateful for the opportunity to help with your cleaning needs!
#
# Based on the info provided, and a special we are running for April, your initial reset clean will be ${initial} (this clean will be 2-3x as long and includes washing all interior window panes within arms reach) and monthly service is ${recuring}.
#
# Please let me know if you would like to get on the schedule and if you have any preferred days/times. Our schedule fills up quickly (especially for the longer initial clean!), but we still have a few spots in April! What works best?
#
# We look forward to cleaning for you!
# {username}
#     """]
#     return scripts[part_list]


def get_quote_text(initial, recuring, part_list, name="there", username="", sqft=0, beds=0, baths=0):
    scripts = [f"""Hi {name}! {username} with Clean Affinity here! 
Thank you for reaching out! 

Based on your address it looks like {sqft} sqft, with {beds} beds and {baths} baths. If that’s correct, your one-time clean will be ${initial} with our April special. 

Is this something I can get on the schedule for you?
""", f"""Hi {name}! {username} with Clean Affinity here! 
Thank you for reaching out! 

Based on your address it looks like {sqft} sqft, with {beds} beds and {baths} baths. If that’s correct, your moving clean will be ${initial} with our April special. 

Is this something I can get on the schedule for you?
""", f"""Hi {name}! {username} with Clean Affinity here! 
Thank you for reaching out! 

Based on your address it looks like {sqft} sqft, with {beds} beds and {baths} baths. If that’s correct, your initial clean will be ${initial} and the following weekly cleans will be ${recuring} with our April special. 

Is this something I can get on the schedule for you?
""", f"""Hi {name}! {username} with Clean Affinity here! 
Thank you for reaching out! 

Based on your address it looks like {sqft} sqft, with {beds} beds and {baths} baths. If that’s correct, your initial clean will be ${initial} and the following biweekly cleans will be ${recuring} with our April special. 

Is this something I can get on the schedule for you?
""", f"""Hi {name}! {username} with Clean Affinity here! 
Thank you for reaching out! 

Based on your address it looks like {sqft} sqft, with {beds} beds and {baths} baths. If that’s correct, your initial clean will be ${initial} and the following monthly cleans will be ${recuring} with our April special. 

Is this something I can get on the schedule for you?
"""]
    return scripts[part_list]
