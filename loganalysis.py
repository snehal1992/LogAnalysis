#! /usr/bin/python3
import psycopg2
import sys


def connect(db_name="news"):
    try:
        conn = psycopg2.connect("dbname=news")
        cursor = conn.cursor()
        return conn, cursor
    except psycopg2.Error as e:
        print("Unable to connect to database")
        sys.exit(1)


def fetch_query(query):
    conn, cursor = connect()
    results = cursor.execute(query)
    results1 = cursor.fetchall()
    conn.close()
    return results1


def print_top_articles():
    results = fetch_query('''
        SELECT title, C
        FROM articles
        JOIN (
        SELECT path
        AS slug , count(*) AS C
        FROM  log
        WHERE length(path) > 11
        GROUP BY path
        ORDER BY (C) DESC limit 3)
        AS logSlug
        on '/article/' || articles.slug = logSlug.slug
        ORDER BY(C) DESC;
        ''')
    with open('results.txt', 'w') as f:
        f.write("1. What are the most popular three articles of all time? \n\n")
        for row in results:
            f.write("%s - %s views \n" %
                    (row[0], row[1]))


def print_top_authors():
    results = fetch_query('''
        CREATE view Temp1 AS (
            SELECT substring(path,10) AS title , count(*) AS C
            FROM log
            GROUP BY path
            ORDER BY (C) DESC
        );
        SELECT DISTINCT name , SUM(c)
        FROM (
        SELECT *
        FROM articles INNER JOIN authors
        ON articles.author = authors.id
        ) AS DB1
        JOIN Temp1
        ON DB1.slug = Temp1.title
        GROUP BY (name)
        ORDER BY SUM(c) DESC;
        ''')
    with open('results.txt', 'a') as f:
        f.write("\n2. Who are the most popular article authors of all time? \n\n")
        for row in results:
            f.write("%s - %s views \n" % (row[0], row[1]))


def print_top_error_days():
    results = fetch_query('''
        CREATE view part3 AS (
        SELECT time::date AS date , count(*)
        AS total  FROM log GROUP BY time::date);

        CREATE view part32 AS  (
        SELECT time::date AS date , count(*) error
        FROM log
        WHERE status = '404 NOT FOUND'
        GROUP BY time::date);

        SELECT part3.date, error/(total*1.0) *100 AS Error
        FROM part3
        JOIN part32
        on part3.date = part32.date
        WHERE error/(total*1.0)  > 0.01;
        ''')

    with open('results.txt', 'a') as f:
        f.write("\n3. On which days did more than 1% of requests lead to errors?\n\n")
        for row in results:
            f.write("%s - %s %% error \n" %
                    (row[0], round(row[1], 2)))


if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_top_error_days()
