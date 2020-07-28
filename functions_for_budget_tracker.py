import json
import ast
import nltk
import argparse
from datetime import datetime

categories = ["rent", "travel", "transit", "gym", "donations", "food", "discretionary"]
valid_actions = ["add", "set budget", "report card", "breakdown", "options", "reset"]
blank_expenses = """{'rent': {'budget': 0, 'spent': 0, 'items': {}},
                'travel': {'budget': 0, 'spent': 0, 'items': {}},
                'transit': {'budget': 0, 'spent': 0, 'items': {}},
                'gym': {'budget': 0, 'spent': 0, 'items': {}},
                'donations': {'budget': 0, 'spent': 0, 'items': {}},
                'food': {'budget': 0, 'spent': 0, 'items': {}},
                'discretionary': {'budget': 0, 'spent': 0, 'items': {}}}"""


### UTILITIES ###


def find_closest(entry, choices=valid_actions, threshold=0.2):
    # Find closest choice for word entered among valid choices based on edit distance
    for choice in choices:
        ed = nltk.edit_distance(choice, entry) / len(choice)
        if ed < 0.2:
            return choice
    return entry


def manage_ledger(action, ledger=None, filename="expenses.json"):
    # Load and save JSON file containing saved ledger

    if action == "open":
        with open(filename, "r") as fp:
            ledger = json.load(fp)
        return ledger

    if action == "close":
        with open(filename, "w") as fp:
            json.dump(ledger, fp)


def reset_all(filename, to_erase="spent"):
    # budget_or_spent should be: "budget", "spent", or "both"py
    ledger = manage_ledger("open", filename=filename)
    if to_erase == "both":
        ledger = ast.literal_eval(blank_expenses)
    elif to_erase == "spent":
        for category in ledger.keys():
            ledger[category][to_erase] = 0
            ledger[category]["breakdown"] = {}
    else:
        for category in ledger.keys():
            ledger[category][to_erase] = 0

    manage_ledger("close", ledger=ledger)


### MANAGEMENT ###


def enter_item(action, ledger, details):
    # Enter a spending or saving amount

    if action == "spending":

        category, amount, item = details.split(" ")
        category, amount, item = category.strip(" "), float(amount), item.strip(" ")
        category = find_closest(entry, choices=categories)  # account for misspellings
        focus = ledger[category]

        focus["spent"] = focus["spent"] + amount
        if item not in focus["breakdown"].keys():
            focus["breakdown"][item] = amount
        else:
            focus["breakdown"][item] = focus["breakdown"][item] + amount
        return ledger

    if action == "budget":

        category, amount = details.split(" ")
        category, amount = category.strip(" "), float(amount)
        focus = ledger[category]

        focus["budget"] = amount
        return ledger


def add_record(action, fn, details):
    # Open ledger, enter item, close ledger
    ledger = manage_ledger("open", filename=fn)
    ledger = enter_item(action, ledger, details)
    manage_ledger("close", ledger=ledger)

    if action == "spending":
        report_card(ledger)


### REPORTING ###


def report_card(filename):
    # Print out spending by category

    ledger = manage_ledger("open", filename=filename)

    rc = "\n"
    rc = rc + "MONTH TO DATE: {}".format(datetime.now().strftime("%B")) + "\n"

    total_spent = 0
    for category in ledger.keys():
        if ledger[category]["spent"] > 0:
            report = round(
                (ledger[category]["spent"] / ledger[category]["budget"]) * 100
            )
            if report >= 80:
                rc = rc + "EIGHTY PERCENT USED" + "\n"
            if report >= 100:
                rc = rc + "NO MORE BUDGET FOR {}".format(category) + "\n"
            total_spent += ledger[category]["spent"]
            rc = (
                rc
                + "{}: {}% (${})".format(
                    category.title(),
                    str(report),
                    "{:.2f}".format(ledger[category]["spent"]),
                )
                + "\n"
            )

    rc = rc + "Total Spent: ${:.2f}".format(total_spent) + "\n"

    manage_ledger("close", ledger=ledger, filename=filename)

    return rc


def report_on_item(filename, category):
    ledger = manage_ledger("open", filename)
    category = ledger[category]
    report = "\n" + "Budget: {}".format(category["budget"]) + "\n"
    report = report + "Spent: {}".format(category["spent"]) + "\n"
    report = report + "On: {}".format(category["breakdown"])
    manage_ledger("close", ledger=ledger)
    return report


def display_options(categories=categories, actions=valid_actions):
    print("The possible actions are: {}".format(", ".join(actions)))
    print("The default categories are: {}".format(", ".join(categories)))
