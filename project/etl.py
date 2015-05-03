import psycopg2
import psycopg2.extras
import datetime

try:
    conn = psycopg2.connect(database="db_investigation", user="admin", password="admin", host="localhost", port="5432")
except:
    print("can not connect the database")

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def load_users():
    cur_internal = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur_internal.execute("""SELECT * from dim_company""")
    except:
        print("I can't SELECT from dim_time")

    rows_internal = cur_internal.fetchall()

    if len(rows_internal) > 0 :
        # already loaded
        print(" users already loaded")
    else:
        print("populate users")
        cur_internal.execute("INSERT INTO dim_company (idw_company, id, name, description, link, user_name) VALUES (1, %s, %s, %s, %s, %s)", [int(194904217218699), "Pepsi Bolivia", "pepsi bolivia", "http://pepsibolivia.com", "pepsibolivia"])
        cur_internal.execute("INSERT INTO dim_company (idw_company, id, name, description, link, user_name) VALUES (2, %s, %s, %s, %s, %s)", [int(237111742996585), "Oriental Mirinda", "oriental mirinda", "http://orientalmirinda.com", "orientalmirinda"])
        conn.commit()

def load_categories():
    cur_internal = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur_internal.execute("""SELECT * from dim_category""")
    except:
        print("I can't SELECT from dim_category")

    rows_internal = cur_internal.fetchall()

    if len(rows_internal) > 0 :
        # already loaded
        print("categories already loaded")
    else:
        print("populate categories")
        cur_internal.execute("INSERT INTO dim_category (idw_category, category, description) VALUES (1, %s, %s)", ["Food/beverages", "Food and beverages"])
        conn.commit()


def load_social_network():
    cur_internal = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur_internal.execute("""SELECT * from dim_social_network""")
    except:
        print("I can't SELECT from dim_category")

    rows_internal = cur_internal.fetchall()

    if len(rows_internal) > 0 :
        # already loaded
        print("social networks already loaded")
    else:
        print("populate social networks")
        cur_internal.execute("INSERT INTO dim_social_network (idw_social_network, name, description, url) VALUES (1, %s, %s, %s)", ["Facebook", "Facebook social network", "http://www.facebook.com"])
        cur_internal.execute("INSERT INTO dim_social_network (idw_social_network, name, description, url) VALUES (2, %s, %s, %s)", ["Twitter", "Twitter social network", "http://www.twitter.com"])
        conn.commit()


def load_weighting():
    cur_internal = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur_internal.execute("""SELECT * from dim_weighting""")
    except:
        print("I can't SELECT from dim_weighting")

    rows_internal = cur_internal.fetchall()

    if len(rows_internal) > 0 :
        # already loaded
        print("social networks already loaded")
    else:
        print("populate weighting")
        cur_internal.execute("INSERT INTO dim_weighting (idw_weighting, segment, weighting, description) VALUES (1, %s, %s, %s)", ["Low", 1, "Low repetition of the string"])
        cur_internal.execute("INSERT INTO dim_weighting (idw_weighting, segment, weighting, description) VALUES (2, %s, %s, %s)", ["Medium-Low", 2, "Medium-Low repetition of the string"])
        cur_internal.execute("INSERT INTO dim_weighting (idw_weighting, segment, weighting, description) VALUES (3, %s, %s, %s)", ["Medium", 3, "Medium repetition of the string"])
        cur_internal.execute("INSERT INTO dim_weighting (idw_weighting, segment, weighting, description) VALUES (4, %s, %s, %s)", ["Medium-High", 4, "Medium-High repetition of the string"])
        cur_internal.execute("INSERT INTO dim_weighting (idw_weighting, segment, weighting, description) VALUES (5, %s, %s, %s)", ["High", 5, "High repetition of the string"])
        conn.commit()

# verify dim_time content
try:
    cur.execute("""SELECT * from dim_time""")
except:
    print("I can't SELECT from dim_time")

rows = cur.fetchall()

if len(rows) > 0 :
    print("table has content lets populate it")
    load_users()
    load_categories()
    load_social_network()
    load_weighting()

else:
    print("table does not have content")
    # creating dates from 1-1-2013 to 1-1-2100
    date_base = datetime.datetime.strptime('01012013', "%d%m%Y").date()
    date_end = datetime.datetime.strptime('01012100', "%d%m%Y").date()
    cursor = conn.cursor()

    while date_base < date_end:
        cursor.execute("INSERT INTO dim_time (idw_date, year, month, day, month_string, day_string, week, week_string) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [date_base, int(date_base.strftime('%Y')), int(date_base.strftime('%m')), int(date_base.strftime('%d')), date_base.strftime('%B'), date_base.strftime('%A'), int(date_base.strftime('%U')), date_base.strftime('%U')])
        date_base = date_base + datetime.timedelta(days=1)

    conn.commit()
    load_users()
    load_categories()
    load_social_network()
    load_weighting()