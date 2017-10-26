#Readme 

##Installation

* Run   `python loganalysis.py` in vagrant environment

* Output : Stored in results.txt file
   

##Views created for part 2 , 3 of the queries

Part 2 : created view to extract title and count from log file 

	create view Temp1 as ( select substring(path,10) as title , count(*) as C  from log group by path order by (C) DESC);

Part 3 : create 2 view -- 

One for storing count of errors by date 

	create view part3 as (select time::date as date , count(*) as total  from log group by time::date);

One for storing total count by date

    create view part32 as  (select time::date as date , count(*) error  from log where status = '404 NOT FOUND' group by time::date);