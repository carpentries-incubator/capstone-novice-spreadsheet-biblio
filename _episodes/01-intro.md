---
title: "Loading data directly into the database"
teaching: 45
exercises: 15
questions:
- "How do we quickly explore data from multiple spreadsheets"
- "Is direct loading of data into a database from random CSVs wise?"
- "What is the ETL process?"
objectives:
- "Explore the difficulties of working with someone else's spreadsheet."
- "Explore the advantages of a quickly made database to answer research questions."
keypoints:
- "Spreadsheets are inflexible and can present challenges when needing to answer novel questions."
- "It is easier to load data into a database than one might think."
- "Dirty data is evil"
---

# What's the point?

Almost everything we can do in a database can be done with sufficiently complex spreadsheets. However, when operating on clean(ish) data, spreadsheets allow us to transform large amounts of data in consistent and reliable ways without needing to *see* the data we are manipulating. 

None of the examples we are covering today is so large that it would cause a modern spreadsheet program to crash. With that said, the 57,254 rows in `2016Census_G01_AUS_SA1.csv` are balky and difficult to work with when we are scrolling around, creating named ranges, and working on multiple layers of comparison. 

The single main benefit of SQL over a spreadsheet that we are covering today is the idea of a `JOIN.` Spreadsheets can certainly perform join-like operations, but the steps are many, specific to each join, and are not reusable. Whereas with SQL, since every output of a query is itself a table which can be used to input into other queries, we not only can JOIN multiple sets of data together, but we can do it with a single line of code. 

The main drawbacks of SQL over a spreadsheet is that you have to *write* that code and that you have to have clean data. (Cue Monty Python Spanish Inquisition sketch here.) However, because each query can produce output used in subsequent queries, we don't have to deal with that complexity all at the same time. Instead, we can gradually creep up on our desired output, making sure of our footing at each step.

We will end this first chapter by joining data from different data sources to answer a rather silly research question: 

> ## A totally not staged question
> I wonder, what's the demographic impact of each political party in Australia on Twitter. @DenubisX - gimme some numbers!
>
>By [Petra Janouchová](https://twitter.com/pettulda/status/1012270311927001088)
{: .testimonial}


# Let's Play with some data.

In this session we will be working with a number of different datasets:

* The [scraped list of australian politicians]({{page.root}}/data/20180628-austmpdata.csv) from the [Library Carpentry Webscraping session](https://resbazsql.github.io/lc-webscraping/). {% comment %}FIXME change the url to the proper lc site after lesson tested and pushed to the carpentries {%endcomment%}
* [Excerpted Data]({{page.root}}/data/2016Census_G01_AUS_SA1.csv) from the [2016 Australian Census](https://datapacks.censusdata.abs.gov.au/datapacks/)
* [Geographic Electoral Division data]({{page.root}}/data/CED_2017_AUST.csv) from the [Australian Bureau of Statistics](http://www.abs.gov.au/ausstats/abs@.nsf/Lookup/by%20Subject/1270.0.55.003~July%202016~Main%20Features~Commonwealth%20Electoral%20Divisions%20(CED)~12)
* And [scraped bibliographic data]({{page.root}}/data/bibliography.csv) using a lightweight [webscraper for Google scholar](https://github.com/ckreibich/scholar.py)

Right now, however, we need to load data directly into a database. Download [this zip file]({{page.root}}/data/mpTwitterAndBiblio.zip) of all the data we will be using in this course.

> ## Direct database csv loading
>
> CSV, comma separated values, or "flat-file" files are one of the preferred means of exhanging data produced from spreasheets and databases. When the data is produced directly from a computer, for a computer's consumption, it is very easy to load. However, this process is fragile and when we are dealing with "denormalized" data, we will have to perform cleaning steps before the data is ready for use.
{: .callout}

While we can enter queries directly into our database, this approach does not scale well when we need to make tweaks to complex queries or we need to write a series of queries to get the data we want. Therefore, we want to make our scripts in a text editor.

Extract the zip file above. It should have the following structure:

~~~
$  ls -F aust_mp_twitter_data/ bibliography_data/
~~~
{: .source .language-bash}

~~~
aust_mp_twitter_data/:
2016Census_G01_AUS_SA1.csv  20180628-austmpdata.csv  CED_2017_AUST.csv

bibliography_data/:
bibliography.csv
~~~
{: .output }

While we are going to turn all of these commands into a script later, let us start by exploring the sqlite3 interface.

run:

~~~
$ sqlite3
~~~
{: .language-bash}

You should see:
~~~
SQLite version 3.22.0 2018-01-22 18:45:57
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> 
~~~
{: .output}

> ## In-memory databases
> 
> By running sqlite3 without a database name, we are creating an in-memory database. This database will evaporate as soon as we quit the program, which is very useful for initial explorations of data or temporary manipulations without needing to run commands to delete and remake whole database.
{: .callout}

Let's run that `.help` command.

Here are the commands we are interested in right now:

| command | explanation |
| --- | --- |
| .import FILE TABLE | Import data from FILE into TABLE |
| .mode CSV | Sets the input and output modes to csv |
| .separator COL | Change the column separator ... for both the output mode and .import |
| .tables | List names of tables |
| .read FILENAME | Execute SQL in FILENAME |


> ## .mode csv
> The sqlite .help command says "output," but if we forget to run it and look in the manual, we learn: 
> ~~~
> Note that it is important to set the "mode" to "csv" before running the ".import" command. This is necessary to prevent the command-line shell from trying to interpret the input file text as some other format.
> ~~~
> {: .blockquote}
> [SQLite manual](https://www.sqlite.org/cli.html#csv_import)
{: .callout}


Now, let us see if we can load some data.
In sqlite:
~~~
sqlite> .mode csv
sqlite> .import aust_mp_twitter_data/20180628-austmpdata.csv austmpdata
~~~
{: .source .language-sql}


Now let us look at the data to see if it's viable for us to work with.

~~~
sqlite> .mode column
sqlite> .header on
sqlite> SELECT * FROM austmpdata LIMIT 5;
~~~
{: .source .language-sql}

We should see something like
~~~
district                    link                                                                  name                party                       phonenumber     twitter                         
--------------------------  --------------------------------------------------------------------  ------------------  --------------------------  --------------  --------------------------------
Warringah, New South Wales  https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=EZ5  Hon Tony Abbott MP  Liberal Party of Australia  (02) 9977 6411  http://twitter.com/TonyAbbottMHR
Bennelong, New South Wales  https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=M3M  Mr John Alexander   Liberal Party of Australia  (02) 9869 4288  http://twitter.com/JohnAlexander
Grayndler, New South Wales  https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=R36  Hon Anthony Albane  Australian Labor Party      (02) 9564 3588  http://twitter.com/AlboMP       
Mallee, Victoria            https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=303  Mr Andrew Broad MP  The Nationals                               https://twitter.com/broad4mallee
McMahon, New South Wales    https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=DZS  Hon Chris Bowen MP  Australian Labor Party      (02) 9604 0710  http://twitter.com/Bowenchris 
~~~
{: .output}

We can then verify the table by calling:

~~~
sqlite> .schema austmpdata
~~~
{: .source}

~~~
CREATE TABLE austmpdata(
  "district" TEXT,
  "link" TEXT,
  "name" TEXT,
  "party" TEXT,
  "phonenumber" TEXT,
  "twitter" TEXT
);
~~~
{: .output .language-sql}


This output is a maximally generic table -- but it is a table which holds our data. This is nothing we couldn't do in a spreadsheet. Yet.

However, now let us try to get data from multiple tables at the same time.

## Writing a script to load our research database

The first thing we need to do is to write a script to load the database. 

Make a file called `aust_mp.sql`

~~~
.echo on
.mode csv
.import aust_mp_twitter_data/20180628-austmpdata.csv austmp
.import aust_mp_twitter_data/2016Census_G01_AUS_SA1.csv census
.import aust_mp_twitter_data/CED_2017_AUST.csv ced

.mode column
.header on


SELECT * 
  FROM census 
 LIMIT 1;

SELECT * 
  FROM austmp
 LIMIT 5;

SELECT * 
  FROM ced 
 LIMIT 5;

SELECT COUNT(*) 
  FROM austmp;
SELECT COUNT(*) 
  FROM census;
SELECT COUNT(*) 
  FROM ced;
~~~
{: .source .language-sql}

> ## Sanity checks
> It is always important to have sanity checks when loading other peoples' data. Running `count(*)` counts the number of rows imported (which can be verified against a row count `wc -l` and `SELECT * FROM table LIMIT 5`.)
{: .callout}

Now, let's run it.

~~~
sqlite> .read aust_mp.sql
~~~

You should see:

~~~
.mode csv
.import aust_mp_twitter_data/20180628-austmpdata.csv austmp
.import aust_mp_twitter_data/2016Census_G01_AUS_SA1.csv census
.import aust_mp_twitter_data/CED_2017_AUST.csv ced

.mode column
.header on


SELECT * 
  FROM census 
 LIMIT 1;
SA1_7DIGITCODE_2016  Tot_P_M     Tot_P_F     Tot_P_P     Age_0_4_yr_M  Age_0_4_yr_F  (...)
-------------------  ----------  ----------  ----------  ------------  ------------  
1100701              140         116         256         6             7             (...)

SELECT * 
  FROM austmp 
 LIMIT 5;
district                    link                                                                  name                party                       phonenumber     twitter                         
--------------------------  --------------------------------------------------------------------  ------------------  --------------------------  --------------  --------------------------------
Warringah, New South Wales  https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=EZ5  Hon Tony Abbott MP  Liberal Party of Australia  (02) 9977 6411  http://twitter.com/TonyAbbottMHR
Bennelong, New South Wales  https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=M3M  Mr John Alexander   Liberal Party of Australia  (02) 9869 4288  http://twitter.com/JohnAlexander
Grayndler, New South Wales  https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=R36  Hon Anthony Albane  Australian Labor Party      (02) 9564 3588  http://twitter.com/AlboMP       
Mallee, Victoria            https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=303  Mr Andrew Broad MP  The Nationals                               https://twitter.com/broad4mallee
McMahon, New South Wales    https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=DZS  Hon Chris Bowen MP  Australian Labor Party      (02) 9604 0710  http://twitter.com/Bowenchris   

SELECT * 
  FROM ced 
 LIMIT 5;
SA1_MAINCODE_2016  CED_CODE_2017  CED_NAME_2017  STATE_CODE_2017  STATE_NAME_2017  AREA_ALBERS_SQKM
-----------------  -------------  -------------  ---------------  ---------------  ----------------
11901135801        101            Banks          1                New South Wales  0.1146          
11901135802        101            Banks          1                New South Wales  0.0722          
11901135803        101            Banks          1                New South Wales  0.1597          
11901135804        101            Banks          1                New South Wales  0.173           
11901135805        101            Banks          1                New South Wales  0.108           

SELECT COUNT(*) 
  FROM austmp;
COUNT(*)  
----------
145       
SELECT COUNT(*) 
  FROM census;
COUNT(*)  
----------
57523     
SELECT COUNT(*) 
  FROM ced;
COUNT(*)  
----------
57523 
~~~
{: .output :language-sql}

Looking at the output above, there should be a moment of "Huh, that's funny." at the `COUNT(*)` of the `ced` table and the `census` table. However, if we look at the `SELECT *` above, we can indeed see different data. The reason that they have the same number of rows is that they're both working off of the Australian Bureau of Statistics "Statistical Area 1" identifiers. 


> ## Exercise
>
> Let's practice some SQL. Write queries which answer the following questions:
> 
> * Using the `LIKE` operator, which MPs are listed as Doctors? 
> * What is the SUM area of each state?
> 
> ### Hints:
> 
> * The wildcard operator is '%' for LIKE.
> * We need to GROUP BY before we aggregate with SUM
>
> > ## Solution
> > 
> > ~~~
> > SELECT name
> >   FROM austmp
> >  WHERE name LIKE 'Dr%';
> >
> > SELECT state_name_2017, SUM(AREA_ALBERS_SQKM)
> >   FROM ced
> >  GROUP BY state_name_2017;
> > ~~~
> > {: .source .language-sql}
> {: .solution}
{: .challenge}

> ## Discussion
>
> How is this approach different in your experience from working with a spreadsheet? What sort of data cleansing and verification work do you do with imported spreadsheet data? How would we translate that to this process?
{: .discussion}

## Cleaning null values

We're going to continue working in this in-memory database. Because it's not writing to disk, it's exceptionally fast. It also makes sure that any data manipulations we make or errors we make aren't going to stick around.

However, we're not done with our data loading yet. We unfortunately have to clean up some `null` values in our code. Remember that SQL differentiates between an empty string and a null value and that this exceptionally fast and dirty method of data loading doesn't provide much nuance. 

In sqlite run:
~~~
sqlite> .echo off
sqlite> .null -null-
sqlite> SELECT * from austmp where twitter is null limit 5;
sqlite> SELECT * from austmp where twitter = '' limit 5;
~~~

We should expect to see the various members of parliment who don't have recorded Twitter handles to show up in the first query. Unfortunately, they show up in the second. Since `''` counts as a value, we can't run aggregate statistics on it, and so must clean it up.

Let us add to our `austmp.sql` file. Those last two commands are to return the SQLite interface into something slightly nicer to work with when we are interrogating the data. 

~~~
UPDATE austmp
   SET twitter = null
 WHERE twitter = '';

.null -null-

SELECT * 
  FROM austmp 
 WHERE twitter is null 
 LIMIT 5;

.echo off
~~~
{: .source :.language-sql}

Now, quit `sqlite3` and relaunch it. This removes any of our prior database from memory and allows us to start with a clean slate. When we manipulate our data-load process, we will always want to test it with a clean slate.

~~~
sqlite> .read aust_mp.sql
~~~

Which, crucially, shows us:

~~~
district                                link                                                                    name                 party                   phonenumber     twitter   
--------------------------------------  ----------------------------------------------------------------------  -------------------  ----------------------  --------------  ----------
Canberra, Australian Capital Territory  https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=30540  Ms Gai Brodtmann MP  Australian Labor Party  (02) 6293 1344  -null-    
McMillan, Victoria                      https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=MT4    Mr Russell Broadben  Liberal Party of Austr  (03) 5623 2064  -null-    
Isaacs, Victoria                        https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=HWG    Hon Mark Dreyfus QC  Australian Labor Party  (03) 9580 4651  -null-    
Oxley, Queensland                       https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=53517  Mr Milton Dick MP    Australian Labor Party  (07) 3879 6440  -null-    
Melbourne Ports, Victoria               https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=WF6    Hon Michael Danby M  Australian Labor Party  (03) 9534 8126  -null-    
~~~
{: .output}

# Finding linking identifiers

Now we move beyond querying single tables. When dealing with other peoples' data, finding what can serve as an identifier can take some time and usually messing about.

If we characterise the 3 csv files using `head -2 *.csv` we see:

~~~
==> aust_mp_twitter_data/2016Census_G01_AUS_SA1.csv <==
SA1_7DIGITCODE_2016,Tot_P_M,Tot_P_F,Tot_P_P,Age_0_4_yr_M,Age_0_4_yr_F,Age_0_4_yr_P,(...)
1100701,140,116,256,6,7,8(...)

==> aust_mp_twitter_data/20180628-austmpdata.csv <==
district,link,name,party,phonenumber,twitter
"Warringah, New South Wales",https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=EZ5,Hon Tony Abbott MP,Liberal Party of Australia,(02) 9977 6411,http://twitter.com/TonyAbbottMHR

==> aust_mp_twitter_data/CED_2017_AUST.csv <==
"SA1_MAINCODE_2016","CED_CODE_2017","CED_NAME_2017","STATE_CODE_2017","STATE_NAME_2017","AREA_ALBERS_SQKM"
"11901135801","101","Banks","1","New South Wales",0.1146
~~~
{: .output}

We can see two places we can link:

* austmpdata: `district` can link to ced: `CED_NAME_2017` + `. ` + `STATE_NAME_2017`
* census: `SA1_7DIGITCODE_2016` can link to the last 7 digits of ced: `SA1_MAINCODE_2016`.

Much of the art of using SQL for csv analysis is finding ways to link data. 

Now we need to create `VIEW`s with those links as new columns.

> ## What is a `VIEW`?
>
> One of the fundamentals of a relational database is that every query's output can be used as an input to other queries. In this lesson, we will be using the idea of a `VIEW` to provide that capability. A view is a stored query with its own name which can be treated like a table. There are other ways to accomplish this objective, but this way allows us to split up the steps more.
{: .callout}

Let us find the queries we want to encode first. We know that ced needs to have a new column with: `CED_NAME_2017` + `. ` + `STATE_NAME_2017`, and that we need the last 7 digits of `SQ1_MAINCODE_2016`. The concatenation operator is `||` and the [SQLite manual](https://www.sqlite.org/lang_corefunc.html) defines `substr(X,Y)` as: "substr(X,Y) returns all characters through the end of the string X beginning with the Y-th."

Let's try:

~~~
sqlite> SELECT ced_name_2017 || ', ' || state_name_2017 as district, substr(sa1_maincode_2016, 5)
  FROM ced
 LIMIT 2; 

sqlite> SELECT sa1_7digitcode_2016
  FROM census
 LIMIT 2;

sqlite> SELECT district
  FROM austmp
 LIMIT 2;
~~~
{: .source :language-sql}

This produces reasonable output, so now let's build it into a `VIEW`.

Editing `aust_mp.sql` add to the end:

~~~
CREATE VIEW ced_district_maincode as
SELECT *, ced_name_2017 || ', ' || state_name_2017 as district, substr(sa1_maincode_2016, 5) as sa1_7digitcode_2016
  FROM ced; 

SELECT * 
  FROM ced_district_maincode 
 LIMIT 2;
~~~
{: .source .language-sql}

Note well that we are removing the `LIMIT` here, because we want this `VIEW` to give us all of the data.

# Answering the research question

Quit and reload `sqlite3` and rerun `.read aust_mp.sql`

Now it is time to join data and answer the research question asked above:


> What is the demographic impact of each political party in Australia on Twitter


We're going to operationalise that as: "The sum of the people in each district, grouped by party, whose MP is on twitter." 

## Joining tables

Since we constructed the view previously, we now need to use that `ced_district_maincode` VIEW to JOIN the other two tables.

Let's try:

~~~
SELECT name, district, Tot_P_P
  FROM austmp
  JOIN ced_district_maincode USING (district)
  JOIN census USING (sa1_7digitcode_2016)
limit 2;
~~~
{: .source .language-sql}

And we get:
~~~
name                  district                Tot_P_P   
--------------------  ----------------------  ----------
Hon David Coleman MP  Banks, New South Wales  443       
Hon David Coleman MP  Banks, New South Wales  244       
~~~
{: output}

We now have taken the names of the MPs scraped from the website and joined them to data gathered in the census by linking the district name and sa1 maincode. 


Now we need a `WHERE` clause.

~~~
SELECT name, district, Tot_P_P
  FROM austmp
  JOIN ced_district_maincode USING (district)
  JOIN census USING (sa1_7digitcode_2016)
 WHERE twitter is not null
LIMIT 2;
~~~
{: .source .language-sql}

And now, instead of focusing on the MP, we need to aggreate on the party:

~~~
SELECT party, sum(Tot_P_P)
  FROM austmp
  JOIN ced_district_maincode USING (district)
  JOIN census USING (sa1_7digitcode_2016)
 WHERE twitter is not null
 GROUP BY party;
~~~
{: .source .language-sql}

Success!

~~~
party              sum(Tot_P_P)
-----------------  ------------
Australian Greens  47431       
Australian Labor   4414595     
Independent        210161      
Katter's Australi  142331      
Liberal Party of   3215790     
The Nationals      1039694 
~~~
{: .output}

> ## Discussion and exercise: What other questions can we ask this data?
> 
> As this is live research data, what other questions can we ask it? Let us, as a class, write some queries on the etherpad to explore this novel dataset. 
{: .discussion}

# Resources

* [SQLite manual](https://www.sqlite.org/lang.html)
* [The Australian Parliament in the Twitterverse](https://search.informit.com.au/documentSummary;dn=201213964;res=IELAPA)

{% include links.md %}
