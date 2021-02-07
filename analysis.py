import sqlite3
from urllib.parse import urlparse


# Create SQLite3 DB connection.
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def get_web_history(chromium_history_file):
    web_history_conn = create_connection(chromium_history_file)

    sql = """
    select u.url as url,
    datetime(v.visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime') AS visit_start,
    datetime((v.visit_time + visit_duration) / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime') AS visit_end
    from visits v
    left join urls u on u.id = v.url;
    """

    cursor = web_history_conn.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()

    return records


def record_emotions_for_url(history_record, emotions_db_file):
    url = history_record[0]
    visit_start = history_record[1]
    visit_end = history_record[2]

    domain = urlparse(url).netloc
    if len(domain.split('.')) > 2:
        domain = '.'.join(domain.split('.')[1:])

    print("{} {} {}".format(domain, visit_start, visit_end))

    # Get all emotions recorded during the visit to this website.
    emotions_conn = create_connection(emotions_db_file)
    sql = "select emotion from emotions where date_time >= '{0}' and date_time <= '{1}'".format(visit_start, visit_end)
    cursor = emotions_conn.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()

    # Add recorded emotions to tracking database.
    for emotion_record in records:
        sql = """INSERT INTO url_emotions(url, emotion, count)
                    VALUES('{0}', '{1}', {2})""".format(domain, emotion_record[0], 1)
        cursor = emotions_conn.cursor()

        try:
            cursor.execute(sql)
            emotions_conn.commit()

        except sqlite3.IntegrityError:
            sql = """UPDATE url_emotions
                        SET count=count+1
                        WHERE url='{0}' AND emotion='{1}'""".format(domain, emotion_record[0])

            cursor.execute(sql)
            emotions_conn.commit()

    return None


def empty_url_emotions_table(emotions_db_file):
    emotions_conn = create_connection(emotions_db_file)

    sql = "DELETE FROM url_emotions"
    cursor = emotions_conn.cursor()
    cursor.execute(sql)
    emotions_conn.commit()

    return None


def main():
    # Get browsing history from Chromium's database.
    web_history = get_web_history("/home/nick/.config/chromium/Default/History")

    # Reload url-emotion correlation table.
    empty_url_emotions_table("emotional_states.db")
    for history_record in web_history:
        record_emotions_for_url(history_record, "emotional_states.db")

    return None


if __name__ == "__main__":
    main()
