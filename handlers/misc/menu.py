from handlers.misc import validation, formatting


def send_title_display(title, description):
    formatting.send_separator_message(title)
    print(description)


def create_menu(title, description, options, back_menu, display_type):
    # Send display aspects
    send_title_display(title, description)

    # Detects input type (int, str)
    if issubclass(display_type, int):
        # Displays menu options, format: "index) option"
        for i in range(len(options)):
            print(str(i+1) + ") " + options[i])
        # Displays back menu option if enabled.
        if back_menu:
            print(str(len(options)+1) + ") Menu")

    elif issubclass(display_type, str):
        # Displays menu options, format "- option"
        for i in range(len(options)):
            print("-", options[i])
        # Displays back menu option if enabled.
        if back_menu:
            print("- Menu")

    print()


def get_menu_response(obj_type, pref, back_menu):
    validated = False
    success, output = None, None
    valid_pref = pref

    # Repeats process of asking for response until validation success
    while not validated:
        response = input("Enter response: ")

        # Detects int class requirement
        if issubclass(obj_type, int):
            # If back menu enabled, it increments the validation boundaries with another index level.
            if back_menu:
                valid_pref[1] += 1
            # Validation output
            success, output = validation.validate_as_int(response, valid_pref)
        # Detects str class requirement
        elif issubclass(obj_type, str):
            # Returns response if no pref
            if pref:
                # If back menu enabled, it appends another option to the pref list, making it valid.
                if back_menu:
                    valid_pref.append("Menu")
                selection = [item.lower() for item in pref]
                # Lowers selections, and compares to see if the index is in the list.
                if response.lower() in selection:
                    # Returns the result choice in the pref list by the index of the lowered comparison.
                    success, output = True, pref[selection.index(response.lower())]
            else:
                success, output = True, response

                if back_menu:
                    if response.lower() == "menu":
                        success, output = True, "Menu"

        # Changes/updates the validation status to the success of the
        validated = success

        if not success:
            validation.error()

    print()
    return output
