import sqlite3 as db
import datetime


# global var
DB_NAME = "record.db"


# functions
def execute_query(sql):
    conn = db.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(sql)
    return conn, cursor


def connect_db():
    # to create expense entry table
    sql = """
    CREATE TABLE IF NOT EXISTS Entry(
        description CHAR(200),
        category CHAR(100),
        date CHAR(8),
        price DECIMAL(10, 2)
    )
    """
    conn, cursor = execute_query(sql)
    conn.commit()


def create_entry(description, category, price):
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d")
    cat = category.lower()
    sql = """
    INSERT INTO Entry VALUES(
    '{}','{}','{}',{}
    )
    """.format(description, cat, date, price)
    conn, cursor = execute_query(sql)
    conn.commit()


# return total price by date (in day month or year by input)
# if invalid date input or entry non-exist -> return None
def calculate_by_date(d):
    date = translate_date(d)
    if date:
        sql = """
            SELECT SUM(price) 
            FROM Entry 
            WHERE date LIKE '{}'
        """.format(date)
        conn, cursor = execute_query(sql)
        # TODO: fix date if entry non exist
        return round(cursor.fetchone()[0], 2)
    else:
        return None


# return total price by category
# if category is None, return total price
def calculate_by_category(category=None):
    if category:
        sql = """
        SELECT SUM(price) 
        FROM Entry 
        WHERE category='{}'
        """.format(category.lower())
    else:
        sql = """
            SELECT SUM(price) 
            FROM Entry
        """
    conn, cursor = execute_query(sql)
    return round(cursor.fetchone()[0], 2)


# list entries by date (in day month or year by input)
# if input invalid -> None
# if no match query -> []
def list_by_date(d):
    date = translate_date(d)
    if date:
        sql = """
            SELECT category, description, price 
            FROM Entry
            WHERE date LIKE '{}'
        """.format(date)
        conn, cursor = execute_query(sql)
        return cursor.fetchall()
    else:
        return date


# list entries by category
# if no match query -> []
def list_by_category(category):
    cat = category.lower()
    sql = """
        SELECT category, description, price 
        FROM Entry
        WHERE category = "{}"
    """.format(cat)
    conn, cursor = execute_query(sql)
    return cursor.fetchall()


def list_all():
    sql = """
        SELECT *
        FROM Entry
    """
    conn, cursor = execute_query(sql)
    return cursor.fetchall()


# user give input date in 3 formats: "yyyy" "yyyymm" "yyyymmdd"
# this function is to translate the input to query: "yyyy____" "yyyymm__" "yyyymmdd"
def translate_date(d):
    if len(d) == 4:
        return d + "____"
    elif len(d) == 6:
        return d + "__"
    elif len(d) == 8:
        return d
    else:
        return None


def validate_date(d):
    return


# connect_db()
# create_entry("coffee", "drinks", 3.49)
print(list_by_date("20200520"))


