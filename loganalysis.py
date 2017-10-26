import psycopg2

conn = psycopg2.connect("dbname=news")

cursor = conn.cursor()

cursor.execute("select  substring(path,10), count(*) as C from log group by path order by (C) DESC limit 3;")

results = cursor.fetchall()
with open('test.txt', 'w') as f:
    for row in results:
        f.write("%s\n" % str(row))

cursor.execute("create view Temp1 as ( select substring(path,10) as title , count(*) as C  from log group by path order by (C) DESC);")
cursor.execute("select distinct name , sum(c)  from (select *  from articles inner  join authors on articles.author = authors.id) as DB1 join Temp1 on DB1.slug = Temp1.title  group by (name) order by sum(c) DESC  ;")
results = cursor.fetchall()
with open('test.txt', 'a') as f:
    for row in results:
        f.write("%s\n" % str(row))

cursor.execute("create view part3 as ( select time::date as date , count(*) as total  from log group by time::date);")
cursor.execute("create view part32 as  (select time::date as date , count(*) error  from log where status = '404 NOT FOUND' group by time::date);")
cursor.execute("select part3.date, error/(total*1.0) *100 as Error from part3 join part32 on part3.date = part32.date where error/(total*1.0)  > 0.01;")
results = cursor.fetchall()
with open('test.txt', 'a') as f:
    for row in results:
        f.write("%s\n" % str(row))

conn.close()