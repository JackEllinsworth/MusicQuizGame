from handlers.misc import formatting, validation

TEMPLATE_FIELDS = [
    {
        "description": "desc",  # Description for display
        "options": [],  # Options to display (for str, display options and valid response list)
        "response_type": int,  # Type of response required (supporting int and str)
        "back_menu": True  # True/False, weather back menu is enabled to cancel menu
    }
]


class Menu:

    def __init__(self, title, fields):
        self.title = title
        self.fields = fields
        self.responses = []

    def get_responses(self):
        # Goes through each field for menu
        for num in range(len(self.fields)):
            # Sends menu display
            self.send(num)
            success, response = None, None

            # Retrieves user input until success
            while not success:
                success, response = self.receive(num)
                # If related to menu response, return to previous menu
                if issubclass(self.fields[num]["response_type"], int) \
                        and response == len(self.fields[num]["options"])+1 and self.fields[num]["back_menu"]:
                    return False, None
                elif issubclass(self.fields[num]["response_type"], str) and self.fields[num]["back_menu"] and \
                        response.lower() == "menu":
                    return False, None

            # Append response
            self.responses.append(response)

        # Return responses and success
        return True, self.responses

    def send(self, field_num):
        field = self.fields[field_num]
        options = field["options"]
        back_menu = field["back_menu"]
        response_type = field["response_type"]

        # Send Title
        formatting.send_separator_message(self.title)

        # Send Description
        print(field["description"])

        # Detects input type (int, str)
        if issubclass(response_type, int):
            # Displays menu options, format: "index) option"
            for i in range(len(options)):
                print(str(i + 1) + ") " + options[i])
            # Displays back menu option if enabled.
            if back_menu:
                print(str(len(options) + 1) + ") Menu")

        elif issubclass(response_type, str):
            if options:
                # Displays menu options, format "- option"
                for i in range(len(options)):
                    print("-", options[i])
                # Displays back menu option if enabled.
                if back_menu:
                    print("- Menu")

        print()

    def receive(self, page_num):
        validated = False
        success, output = None, None
        field = self.fields[page_num]
        back_menu = field["back_menu"]
        options = field["options"]
        response_type = field["response_type"]

        if options:
            options = options.copy()

        # Retrieves user input until validated
        while not validated:
            response = input("Enter response: ")

            # If integer type, retrieves boundaries, adds back menu to boundary if existent, updates success & output
            # Validates and integer
            if issubclass(response_type, int):
                boundaries = [1, len(options)]
                if back_menu:
                    boundaries[1] += 1
                success, output = validation.validate_as_int(response, boundaries)

            # If string type, checks to see if options, if not returns success due to no limits
            elif issubclass(response_type, str):
                if options:
                    # Appends menu to options to respond to, as back_menu is true
                    if back_menu:
                        options.append("Menu")

                    # Lowers all options for string comparison
                    lowered_options = [item.lower() for item in options]
                    # Detects if string is in lowered array, and then returns the formatted string in the options arr
                    if response.lower() in lowered_options:
                        success, output = True, options[lowered_options.index(response.lower())]
                else:
                    # Update success and output as true and the normal response (no modifications)
                    success, output = True, response

            validated = success

            if not success:
                validation.error()

        print()
        return success, output
