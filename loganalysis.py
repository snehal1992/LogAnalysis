#! /usr/bin/python3
import psycopg2


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
    return cursor.fetchall()
    conn.close()


def print_top_articles():
    results = fetch_query(
        "select title, C from articles join (select  substring(path,10)" +
        " as slug , count(*) as C from  log where length(path) > 11  group by path"
        " order by (C) DESC limit 3) as logSlug on articles.slug = logSlug.slug" +
        " order by(C) DESC;")
    with open('results.txt', 'w') as f:
        f.write("1. What are the most popular three articles of all time? \n\n")
        for row in results:
            f.write("%s - %s views \n" %
                    (row[0], row[1]))


def print_top_authors():
    results = fetch_query(
        "create view Temp1 as ( select substring(path,10) as" +
        " title , count(*) as C  from log group by path order by (C) DESC);" +
        "select distinct name , sum(c)  from (select *  from articles" +
        " inner  join authors on articles.author = authors.id)" +
        " as DB1 join Temp1 on DB1.slug = Temp1.title" +
        " group by (name) order by sum(c) DESC ;")
    with open('results.txt', 'a') as f:
        f.write("\n2. Who are the most popular article authors of all time? \n\n")
        for row in results:
            f.write("%s - %s views \n" % (row[0], row[1]))


def print_top_error_days():
    results = fetch_query(
        "create view part3 as ( select time::date as date , count(*)" +
        " as total  from log group by time::date);" +
        "create view part32 as  (select time::date as date ," +
        " count(*) error  from log where status = '404 NOT FOUND'" +
        " group by time::date);" +
        "select part3.date, error/(total*1.0) *100 as Error" +
        " from part3 join part32 on part3.date = part32.date" +
        " where error/(total*1.0)  > 0.01;")
    with open('results.txt', 'a') as f:
        f.write("\n3. On which days did more than 1% of requests lead to errors?\n\n")
        for row in results:
            f.write("%s - %s %% error \n" %
                    (row[0], round(row[1], 2)))


if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_top_error_days()
