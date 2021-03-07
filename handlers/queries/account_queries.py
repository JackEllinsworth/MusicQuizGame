from handlers.db.db_manager import Database
from handlers.db.db_models import Account


def get_account_by_id(database: Database, user_id):
    # Creates the cursor and uses sql to execute the SELECT query.
    cursor = database.connection.cursor()
    cursor.execute("SELECT * FROM ACCOUNTS WHERE ID = ?", (user_id,))
    data = cursor.fetchone()

    # If no data is found, it returns false
    if not data: return False

    # Creates account which has that ID in an Account object for ease.
    new_account = Account(data[0], data[1], data[2], data[3])

    # Closes cursor, and returns account object.
    cursor.close()
    return new_account


def check_for_admins(database: Database):
    # Creates cursor and uses sql to execute SELECT query
    cursor = database.connection.cursor()
    cursor.execute("SELECT * FROM ACCOUNTS WHERE PERMISSION = ?", ("Administrator",))
    result = cursor.fetchone()

    if result:
        return True
    else:
        return False


def get_account_by_name(database: Database, username):
    # Uses SQL Select query to get the accounts via username
    cursor = database.connection.cursor()
    cursor.execute("SELECT * FROM ACCOUNTS WHERE USERNAME = ?", (username,))
    accounts = []
    results = cursor.fetchall()

    # If the length of the results matches more than 1 (>1), it will create an array of accounts.
    # This is so that when logging in, it will match it with all accounts passwords, so you can get the correct
    # account via ID, which is unique to every single account.
    for row in results:
        new_account = Account(row[0], row[1], row[2], row[3])
        accounts.append(new_account)

    # Closes cursor and returns located accounts
    cursor.close()
    return accounts


def overwrite_existing_account(database: Database, account: Account):
    cursor = database.connection.cursor()

    try:
        cursor.execute("""UPDATE ACCOUNTS SET username = ?, password = ?, permission = ? WHERE ID = ?""",
                       (account.retrieve("username"), account.retrieve("password"), account.retrieve("permission"),
                        account.retrieve("userId")))
        cursor.close()
        database.save()
        return True
    except:
        return False


def create_new_account(database: Database, username, password, permission):
    cursor = database.connection.cursor()

    try:
        accounts = get_account_by_name(database, username)

        # Checks to see if account with that name AND password already exists, if it does, it returns false
        if len(accounts) >= 1:
            for i in range(len(accounts)):
                if accounts[i].retrieve("password") == password:
                    return False

        # Executes query and creates account
        cursor.execute("INSERT INTO ACCOUNTS (USERNAME, PASSWORD, PERMISSION) \
                        VALUES (?,?,?)", (username, password, permission))

        cursor.close()
        database.save()
        return True
    except:
        return False