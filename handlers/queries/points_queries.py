from handlers.db.db_models import Points, Account
from handlers.db.db_manager import Database
from handlers.queries import account_queries


# Retrieves top global scores
def retrieve_global_top(database: Database, amount):
    cursor = database.connection.cursor()
    # Executes SQL query, ordering results by the highest points, limiting to (amount)
    cursor.execute("SELECT userId, points, time FROM POINTS ORDER BY points DESC LIMIT ?", (amount,))
    results = cursor.fetchall()
    global_top = []

    # Iterates through results
    for row in results:
        formatted_str = None
        # Retrieves account matching data
        user_acc = account_queries.get_account_by_id(database, row[0])

        # If account exists, updates name and ID
        if user_acc:
            formatted_str += ("Name: " + user_acc.retrieve("username") +
                              " (ID: " + str(user_acc.retrieve("userId")) + ")")
        else:
            # Account doesn't exist anymore, update
            formatted_str += "Name: DELETED_ACC"

        # Formats string and appends to array
        formatted_str += (" | Points: " + str(row[1]) + " | Time: " + str(row[2]))
        global_top.append(formatted_str)

    cursor.close()

    return global_top


def retrieve_local_top(database: Database, account: Account, amount):
    cursor = database.connection.cursor()
    # Retrieves users userId
    account_id = account.retrieve("userId")

    # Executes sql query, searching the points for the highest score from the userId for (userId)
    cursor.execute("SELECT userId, points, time FROM POINTS WHERE userId = ? ORDER BY points DESC LIMIT ?",
                   (account_id, amount))

    local_top = []

    for row in cursor:
        # Appends all results to table, ready for display
        formatted_str = None
        formatted_str += ("Points: " + str(row[1]) + " | Time: " + str(row[2]))
        local_top.append(formatted_str)

    cursor.close()

    return local_top


def create_score_set(database: Database, points: Points):
    cursor = database.connection.cursor()

    # Creates score set on database
    try:
        # Inserts data into points
        cursor.execute("""INSERT INTO POINTS (USERID, POINTS, TIME) \
                        VALUES (?,?,?)""", (points.retrieve("userId"), points.retrieve("points"), points.retrieve("time")))
        cursor.close()
        database.save()
        return True
    except:
        return False


def clear_user_data(database: Database, account: Account):
    cursor = database.connection.cursor()

    try:
        # Retrieves accountId from account object
        account_id = account.retrieve("userId")

        # Deletes anything in points db matching the userId of account_id
        cursor.execute("""DELETE FROM POINTS WHERE userId = ?""", (account_id,))
        cursor.close()
        database.save()
        return True
    except:
        return False
