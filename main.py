from handlers.db.db_manager import Database
from interface import auth_menu

# Load data & initialize connection
db_obj = Database()
db_obj.load()

# Initializes authorization menu
auth_menu.activate(db_obj)
