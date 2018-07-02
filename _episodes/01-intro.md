---
title: "Loading data directly into the database"
teaching: 30
exercises: 10
questions:
- "What is the difference between a spreadsheet and a table?"
- "How do I bulk load data into sqlite3?"
objectives:
- "Explore data from different locations using a single database"
keypoints:
- "Most databases allow people to load data from csv"
- "The default settings on data loading are OK for a quick look at the data"
---

Almost everything we can do in a database can be done with sufficiently complex spreadsheets. However, when operating on clean(ish) data, databases allow us to transform large amounts of data in consistent and reliable ways without needing to *see* the data we are manipulating. 

None of the examples we are covering today is so large that it would cause a modern spreadsheet program to crash. With that said, the 57,254 rows in `2016Census_G01_AUS_SA1.csv` are balky and difficult to work with when we are scrolling around, creating named ranges, and working on multiple layers of comparison. 

The single main benefit of SQL over a spreadsheet that we are covering today is the idea of a `JOIN`. Spreadsheets can certainly perform join-like operations, but the steps are many, specific to each join, and are not reusable. Whereas with SQL, since every output of a query is itself a table which can be used to input into other queries, we not only can `JOIN` multiple sets of data together, but we can do it with a single line of code. 

The main drawbacks of SQL over a spreadsheet is that you have to *write* that code and that you have to have clean data. (Cue Monty Python Spanish Inquisition sketch here.) However, because each query can produce output used in subsequent queries, we don't have to deal with that complexity all at the same time. Instead, we can gradually creep up on our desired output, making sure of our footing at each step.

We will end this first chapter by joining data from different data sources to answer a rather silly research question: 

> ## A totally not staged question
> I wonder, what's the demographic impact of each political party in Australia on Twitter. @DenubisX - gimme some numbers!
>
>By [Petra Janouchová](https://twitter.com/pettulda/status/1012270311927001088)
{: .testimonial}

## Research Question Operationalisation

How can we turn this question into something we can answer? 


> In research design, especially in psychology, social sciences, life sciences, and physics, operationalization is a process of defining the measurement of a phenomenon that is not directly measurable, though its existence is indicated by other phenomena.
> 
> [Wikipedia](https://en.wikipedia.org/wiki/Operationalization)
{: .quotation}


We start with the question: "What can we measure?"

* We know politicans who are on twitter from the list of Australian members of parliament.
* We know what party those politics are from, from the same list.
* We know that the 2016 census has demographic population per "Statistical Area"
* We know that the ABS publishes a dataset which names the regions alongside their statistical identifiers. 

We can therefore ask something like: For members of parliment on twitter, what is the sum total of people in their district, grouped by party?

Granted, this question is entirely contrived, but hopefully plausible in the ability of linking datasets.

We now need to inspect the data files to see if these measurable things are present. 

In this chapter we will be working with a number of different datasets:

* The [scraped list of Australian politicians]({{page.root}}/data/20180628-austmpdata.csv) from the [Library Carpentry Webscraping session](https://resbazsql.github.io/lc-webscraping/). {% comment %}FIXME change the url to the proper lc site after lesson tested and pushed to the carpentries {%endcomment%}
* [Excerpted Data]({{page.root}}/data/2016Census_G01_AUS_SA1.csv) from the [2016 Australian Census](https://datapacks.censusdata.abs.gov.au/datapacks/)
* [Geographic Electoral Division data]({{page.root}}/data/CED_2017_AUST.csv) from the [Australian Bureau of Statistics](http://www.abs.gov.au/ausstats/abs@.nsf/Lookup/by%20Subject/1270.0.55.003~July%202016~Main%20Features~Commonwealth%20Electoral%20Divisions%20(CED)~12)

Download [this zip file]({{page.root}}/data/mpTwitterAndBiblio.zip) of all the data we will be using in this course.


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

If we characterise the 3 csv files in `aust_mp_twitter_data/` using 
~~~
$ head -2 aust_mp_twitter_data/*.csv
~~~
{: .source .language-bash}
we see:

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

We see the following columns of interest:

* `Tot_P_P`. Described by the [Census Metadata]({{page.root}}/data/aust_mp_twitter_data/Metadata/Metadata_2016_GCP_DataPack.xlsx) as: 
~~~
G3  Tot_P_P Total_Persons_Persons G01 G01a  Persons
~~~
* The "SA1 Maincode" columns, suggesting linking; and
* The the "Party" and "Twitter" columns of "our own" web-scraped data. 

To a first approximation, we can answer Petra's question!



> ## Direct database csv loading
>
> CSV, comma separated values, or "flat-file" files are one of the preferred means of exchanging data produced from spreadsheets and databases. When the data is produced directly from a computer, for a computer's consumption, it is very easy to load. However, this process is fragile and when we are dealing with "denormalized" data, we will have to perform cleaning steps before the data is ready for use.
{: .callout}

While we can enter queries directly into our database, this approach does not scale well when we need to make tweaks to complex queries or we need to write a series of queries to get the data we want. Therefore, we want to make our scripts in a text editor.

Let us start by exploring the sqlite3 interface.

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


This output is a maximally generic table -- but it is a table which holds our data. This is nothing we couldn't do in a spreadsheet. [Yet.](https://yarn.co/yarn-clip/4c039198-d848-4228-93a8-896208c04526)

Now, however, let us try to interact with multiple tables at the same time.

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

-- normally we'd want to select * here. But considering how many columns our dataset outputs, it makes for really awful output. Instead, we'll take the columns we care about instead. 

SELECT SA1_7DIGITCODE_2016, Tot_P_M, Tot_P_F, Tot_P_P     
  FROM census 
 LIMIT 5;

SELECT district, party, twitter
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

SELECT SA1_7DIGITCODE_2016, Tot_P_M, Tot_P_F, Tot_P_P     
  FROM census 
 LIMIT 5;
SA1_7DIGITCODE_2016  Tot_P_M     Tot_P_F     Tot_P_P   
-------------------  ----------  ----------  ----------
1100701              140         116         256       
1100702              202         175         381       
1100703              201         228         428       
1100704              189         254         446       
1100705              192         208         402       

SELECT district, party, twitter
  FROM austmp
 LIMIT 5;
district                    party                       twitter                         
--------------------------  --------------------------  --------------------------------
Warringah, New South Wales  Liberal Party of Australia  http://twitter.com/TonyAbbottMHR
Bennelong, New South Wales  Liberal Party of Australia  http://twitter.com/JohnAlexander
Grayndler, New South Wales  Australian Labor Party      http://twitter.com/AlboMP       
Mallee, Victoria            The Nationals               https://twitter.com/broad4mallee
McMahon, New South Wales    Australian Labor Party      http://twitter.com/Bowenchris   

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
> * What is the `SUM()` area of each state?
> 
> ### Hints:
> 
> * The wildcard operator is `%` for `LIKE`.
> * We need to `GROUP BY` before we aggregate with `SUM()`
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

# Resources

* [SQLite manual](https://www.sqlite.org/lang.html)
* [The Australian Parliament in the Twitterverse](https://search.informit.com.au/documentSummary;dn=201213964;res=IELAPA)

{% include links.md %}
