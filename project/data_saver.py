from _sitebuiltins import _Printer
import psycopg2
import psycopg2.extras
import datetime
import time
from pymongo import MongoClient
from operator import itemgetter
import sys


def get_connection():
    try:
        conn = psycopg2.connect(database="db_investigation", user="admin", password="admin", host="localhost", port="5432")
    except:
        print("can not connect the database")

    return conn


def get_distribution(comments_cleaned):
    addition = sum(int(comment[1]) for comment in comments_cleaned)
    print(addition)
    media = addition / len(comments_cleaned)
    q1limit = comments_cleaned[-1][1]
    q2limit = (media + q1limit) / 2
    q3limit = (comments_cleaned[0][1] + media) / 2
    q4limit = comments_cleaned[0][1]

    return (q1limit, q2limit, media, q3limit, q4limit)


def infer_weighting(repetition, distribution):

    q1limit, q2limit, media, q3limit, q4limit = distribution
    if repetition > 0 and repetition <= q1limit:
        answer = 1
    elif repetition > q1limit and repetition <= q2limit:
        answer = 2
    elif repetition > q2limit and repetition <= media:
        answer = 3
    elif repetition > media and repetition <= q3limit:
        answer = 4
    elif repetition > q3limit:
        answer = 5
    else:
        answer = 1

    return answer

def load_data(current_date):
    con = get_connection()
    client = MongoClient('localhost', 27017)
    db = client["socialinteraction"]

    c_date_string = current_date.strftime("%Y-%m-%d")
    c_date = current_date.date()
    c_year = int(current_date.strftime("%Y"))
    c_month = int(current_date.strftime("%m"))
    c_day = int(current_date.strftime("%d"))

    posts = db["fb_posts"].find({'created.0': c_year, 'created.1': c_month, 'created.2': c_day, 'count_comments': {"$ne": ""}})
    tweets = db["tw_posts"].find({'created.0': c_year, 'created.1': c_month, 'created.2': c_day})
    status = db["meta_data"].find_one({'date': c_date_string, 'company': 'pepsibolivia'})

    conn = get_connection()

    if status:
        # save snapshot
        register = False
        cur_internal = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur_internal.execute("SELECT * from fact_social_status WHERE idw_date = %s AND idw_company = 1", [c_date])
            register = cur_internal.fetchone()
        except:
            print("Error selecting data from fact_social_status")

        if not register:
            #register snapshot
            try:
                cur_internal.execute("INSERT INTO fact_social_status (idw_date, idw_company, idw_category, idw_social_network, likes_number, number_unique_people) VALUES (%s, 1, 1, 1, %s, %s)", [c_date, status["likes"], status["talking_about_count"]])
                conn.commit()
            except:
                print("Error selecting data from fact_social_status")


    if((tweets.count() > 0 or posts.count() > 0)):
        print("company: pepsibolivia, lets rock for date:", c_date_string)
        comments = {}
        if tweets.count() > 0:
            for tw in tweets:
                for word in tw["distribution"]:
                    recurrences = comments.get(word[0], 0)
                    if recurrences == 0:
                        comments[word[0]] = 1
                    else:
                        comments[word[0]] += recurrences
        if posts.count() > 0:
            for post in posts:
                for word in post["distribution"]:
                    recurrences = comments.get(word[0], 0)
                    if recurrences == 0:
                        comments[word[0]] = 1
                    else:
                        comments[word[0]] += int(recurrences)

        comments_sorted = sorted(comments.items(), key=itemgetter(1), reverse=True)
        comments_cleaned = comments_sorted[:20]
        #print(comments_cleaned)
        distribution = get_distribution(comments_cleaned)
        media_hardcoded = False
        if distribution[0] == distribution[1] == distribution[3] == distribution[4]:
            # standard weight
            media_hardcoded = 3

        for element in comments_cleaned:
            if media_hardcoded:
                weighting = media_hardcoded
            else:
                weighting = infer_weighting(element[1], distribution)

            # save snapshot
            register = False
            cur_internal = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            try:
                cur_internal.execute("SELECT * from fact_word WHERE idw_date = %s AND idw_company = 1 AND word LIKE %s AND idw_weighting = %s", [c_date, element[0], weighting])
                register = cur_internal.fetchone()
            except:
                print("Error selecting data from fact_word eeee")
            if not register:
                #register data
                try:
                    cur_internal.execute("INSERT INTO fact_word (idw_date, idw_weighting, idw_company, word, repetition, weighting) VALUES (%s, %s, 1, %s, %s, %s)", [c_date, weighting, element[0], element[1], weighting])
                    conn.commit()
                except:
                    print("Error selecting data from fact_word")

today = datetime.datetime.utcnow()
for i in range(1,51):
    new_today = today - datetime.timedelta(days=i)
    load_data(new_today)

