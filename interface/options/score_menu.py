from handlers.db.db_models import Account
from handlers.db.db_manager import Database
from handlers.queries import points_queries
from handlers.misc import menu

SCORE_OPTIONS = ["View global top scores", "View your top scores"]
TOP_AMOUNT = 5


def activate(database: Database, account: Account):
    menu.create_menu("SCORE MENU", "Please select an option below", SCORE_OPTIONS, True, int)
    selected_option = menu.get_menu_response(int, [1, len(SCORE_OPTIONS)], True)
    if selected_option == "Menu": return

    if selected_option == 1:
        formatted_point_sets = points_queries.retrieve_global_top(database, TOP_AMOUNT)
        menu.send_title_display("SCORE MENU: Global Top Scores",
                                "Below are the top " + str(TOP_AMOUNT) + " global scores.\n")

        for i in range(len(formatted_point_sets)):
            print(formatted_point_sets[i])
        print()
    elif selected_option == 2:
        formatted_point_sets = points_queries.retrieve_local_top(database, account, TOP_AMOUNT)
        menu.send_title_display("SCORE MENU: Local Top Scores",
                                "Below are the top " + str(TOP_AMOUNT) + " local scores.\n")

        for i in range(len(formatted_point_sets)):
            print(formatted_point_sets[i])
        print()
