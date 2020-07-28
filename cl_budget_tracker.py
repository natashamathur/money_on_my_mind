from functions_for_budget_tracker import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action")
    parser.add_argument("--filename")
    parser.add_argument("--d")
    args = parser.parse_args()

    ### SET DEFAULTS ###

    if args.filename:
        fn = args.filename
    else:
        fn = "expenses.json"

    # account for misspellings
    requested_action = find_closest(args.action.lower(), choices=valid_actions)
    print("Taking Action: {}".format(requested_action))
    if requested_action not in valid_actions:
        print("Invalid Category")
        display_options()

    # add new expense
    if requested_action == "add":
        if not args.d or len(args.d.split(" ")) < 3:
            print("""Please enter values in the form "food 25 takeout" """)
            quit()

        add_record("spending", fn, args.d)

    ### REPORTING ###

    # get overall budget summary
    if requested_action == "report card":
        print(report_card(fn))

    # get breakdown for specific category
    if requested_action == "breakdown":
        if not args.d:
            print("Please enter the category you want broken down.")
        print(report_on_item(fn, args.d))

    ### HELP ###

    # see all possible options
    if requested_action == "options":
        display_options()

    ### BOOKKEEPING ###

    # set a specific budget item
    if requested_action == "set budget":
        if not args.d or len(args.d.split(" ")) < 2:
            print("""Please enter values in the form "gym 80" """)
            quit()

        add_record("budget", fn, args.d)

    # reset current budget completely
    if requested_action == "reset":
        if args.d in ["spent", "budget"]:
            reset_all(fn, args.d)
        elif args.d:  # If entered invalid args.d
            print("""Please enter either "spent" or "budget" """)
            quit()
        else:
            reset_all(fn)
