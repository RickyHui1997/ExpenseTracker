import sqlite3 as db
import datetime
import xlwt


# global vars
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
    cat = category.strip().lower()
    sql = """
    INSERT INTO Entry VALUES(
    '{}','{}','{}',{}
    )
    """.format(description, cat, date, price)
    conn, cursor = execute_query(sql)
    conn.commit()


# return total price by category and/or by date
# if both are None, return total price
# if invalid date input or entry non-exist -> return None
def calculate_total(category, date):
    c = category.strip().lower() if category else None
    if c and not date:
        sql = """
            SELECT SUM(price)
            FROM Entry
            WHERE category='{}'
        """.format(c)
    elif not c and date:
        d = translate_date(date)
        if d:
            sql = """
                SELECT SUM(price)
                FROM Entry
                WHERE date LIKE '{}'
            """.format(d)
        else:
            return d
    elif c and date:
        d = translate_date(date)
        if d:
            sql = """
                SELECT SUM(price)
                FROM Entry
                WHERE date LIKE '{}' AND category='{}'
            """.format(d, c)
        else:
            return d
    else:
        sql = """
            SELECT SUM(price)
            FROM Entry
        """
    conn, cursor = execute_query(sql)
    return cursor.fetchall()[0][0]


# list entries by date (in day month or year by input)
# if input invalid -> None
# if no match query -> []
def list_by_specific(category, date):
    c = category.strip().lower() if category else None
    if c and not date:
        sql = """
                SELECT *
                FROM Entry
                WHERE category='{}'
            """.format(c)
    elif not c and date:
        d = translate_date(date)
        if d:
            sql = """
                    SELECT *
                    FROM Entry
                    WHERE date LIKE '{}'
                """.format(d)
        else:
            return d
    elif c and date:
        d = translate_date(date)
        if d:
            sql = """
                    SELECT *
                    FROM Entry
                    WHERE date LIKE '{}' AND category='{}'
                """.format(d, c)
        else:
            return d
    else:
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


def export_entries(filename, data):
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Sheet")
    titles = ["Description", "Category", "Date", "Price"]
    for j in range(len(titles)):
        sheet.write(0, j, titles[j])
    row = 1
    for entry in data:
        for col in range(len(entry)):
            sheet.write(row, col, entry[col])
        row += 1
    book.save(filename)
