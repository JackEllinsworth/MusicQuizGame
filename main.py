from handlers.db.db_manager import Database
from interface import menu_init

# Load data & initialize connection
db_obj = Database()
db_obj.load()

# Initializes authorization menu
menu_init.auth_menu(db_obj)
