from handlers.db.db_models import Account
from handlers.db.db_manager import Database
from handlers.queries import points_queries
from handlers.misc.menu import Menu, formatting

SCORE_OPTIONS = ["View global top scores", "View your top scores"]
TOP_AMOUNT = 5


def activate(database: Database, account: Account):
    menu = Menu("SCORE MENU", [
        {
            "description": "Please select an option below",
            "options": SCORE_OPTIONS,
            "response_type": int,
            "back_menu": True
        }
    ])

    success, responses = menu.get_responses()
    if not success: return

    selected_option = responses[0]

    if selected_option == 1:
        formatted_point_sets = points_queries.retrieve_global_top(database, TOP_AMOUNT)
        formatting.send_separator_message("SCORE MENU: Global Top Scores")
        print("Below are the top " + str(TOP_AMOUNT) + " global scores.\n")

        for i in range(len(formatted_point_sets)):
            print(formatted_point_sets[i])
        print()

    elif selected_option == 2:
        formatted_point_sets = points_queries.retrieve_local_top(database, account, TOP_AMOUNT)
        formatting.send_separator_message("SCORE MENU: Local Top Scores")
        print("Below are the top " + str(TOP_AMOUNT) + " local scores.\n")

        for i in range(len(formatted_point_sets)):
            print(formatted_point_sets[i])
        print()
