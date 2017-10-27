# LOG ANALYSIS

Reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database. 

## Installation


* Import the newsdata.sql file - [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and load into desired directory 

* Run   `python loganalysis.py` file  from the same directory 

* Output : Stored in results.txt file
   

## Views created for part 2 , 3 of the queries

Part 2 : 

created view to extract title and count from log file 
```sql
  create view Temp1 as ( 
	select substring(path,10) as title , count(*) as C  
	from log 
	group by path 
	order by (C) DESC
	);
```
Part 3 : 

One for storing count of errors by date 
```sql
	create view part3 as (
		select time::date as date , 
		count(*) as total  
		from log 
		group by time::date
		);
```
One for storing total count by date
```sql
    create view part32 as  (
    	select time::date as date , 
    	count(*) error  
    	from log 
    	where status = '404 NOT FOUND' 
    	group by time::date
    	);
```