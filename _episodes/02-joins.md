---
title: "Combining data sets"
teaching: 30
exercises: 10
questions:
- "What is the essential thing needed to combine data from different sources?"
objectives:
- "Learn how to use a `VIEW` to save a query."
- "Explore `JOIN`ining tables to answer a research question."
keypoints:
- "A `VIEW` can be used to create saved queries which can be used like tables."
- "We can quickly load multiple CSVs into the same database."
- "csvs can be linked if we can find the right key."
---


## Cleaning null values

We're going to continue working in this in-memory database. Because it's not writing to disk, it's exceptionally fast. It also makes sure that any data manipulations we make or errors we make aren't going to stick around.

However, we're not done with our data loading yet. We unfortunately have to clean up some `null` values in our code. Remember that SQL differentiates between an empty string and a null value and that this exceptionally fast and dirty method of data loading doesn't provide much nuance. 

In sqlite run:
~~~
sqlite> .echo off
sqlite> .null -null-
sqlite> SELECT * FROM austmp WHERE twitter is null LIMIT 5;
sqlite> SELECT * FROM austmp WHERE twitter = '' LIMIT 5;
~~~

We should expect to see the various members of parliament who don't have recorded Twitter handles to show up in the first query. Unfortunately, they show up in the second. Since `''` counts as a value, we can't run aggregate statistics on it, and so must clean it up.

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

If we characterise the 3 csv files using `head -2 aust_mp_twitter_data/*.csv` we see:

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

Let's try starting `sqlite3` up once again, rerunning `.read aust_mp.sql` and then: 

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

Since we constructed the view previously, we now need to use that `ced_district_maincode` view to join the other two tables.

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

And now, instead of focusing on the MP, we need to aggregate on the party:

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

> ## Discussion
>
> How long would it have taken to do what we just did using spreadsheets? Would that data be usable for any other question after the fact?

> ## Group exercise: What other questions can we ask this data?
> 
> As this is live research data, what other questions can we ask it? Let us, as a class, write some queries on the etherpad to explore this novel dataset. 
{: .discussion}

# Resources

* [SQLite manual](https://www.sqlite.org/lang.html)
* [The Australian Parliament in the Twitterverse](https://search.informit.com.au/documentSummary;dn=201213964;res=IELAPA)

{% include links.md %}
