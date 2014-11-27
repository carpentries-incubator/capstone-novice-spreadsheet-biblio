---
layout: page
title: From a Spreadsheet to a Database
subtitle: Introduction
minutes: 2
---
> ## Learning Objectives {.objectives}
>
> * Explain why the initial spreadsheet is hard to work with.
> * Explain why a single-table database would be more usable.

Our starting point is a spreadsheet called `bibliography.csv`
with 2937 rows like this:

|key     |type       |year|authors                                                                                           |title             |journal                                             |
|--------|-----------|----|--------------------------------------------------------------------------------------------------|------------------|----------------------------------------------------|
|8SW85SQM|journalArticle|2013|McClelland, James L|Incorporating Rapid Neocortical Learning of New Schema-Consistent Information Into Complementary Learning Systems Theory.|J Exp Psychol Gen|
|85QV9X5F|journalArticle|1995|McClelland, J. L.; McNaughton, B. L.; O'Reilly, R. C.|Why There are Complementary Learning Systems in the Hippocampus and Neocortex: Insights from the Successes and Failures of Connectionist Models of Learning and Memory|Psychological Review|
|Z4X6DT6N|journalArticle|1990|Ratcliff, R.|Connectionist models of recognition memory: constraints imposed by learning and forgetting functions.|Psychological review|

We'd like to know:

*   How many papers has each person contributed to?

*   Who collaborates with whom?

If we only cared about one author,
we could search for her name in the spreadsheet to answer the first question,
then select those rows and manually tally her co-authors to answer the second.
But doing that for all of the authors one by one would take days,
we'd almost certainly make mistakes,
and then someone would almost certainly hand us another, larger spreadsheet
and we'd have to start over.

Here's what we're going to do instead:

1.  Write a little Python program to print (key, author) pairs for every contributor to every paper.
    For example,
    this program will turn the first three rows of the spreadsheet into:

    ~~~
    8SW85SQM McClelland, James L
    85QV9X5F McClelland, J. L.
    85QV9X5F McNaughton, B. L.
    85QV9X5F O'Reilly, R. C.
    Z4X6DT6N Ratcliff, R.
    ~~~

2.  Create an SQL database with one table called `authors`
    and insert each (key, author) pair into that table.

3.  Use SQL queries to answer our original questions.

This might seem like a lot of work to answer two questions,
but it's the right approach for several reasons:

*   Once the data is in a database,
    it will be easy to ask and answer many other questions.

*   We'll be able to re-use our tools on the next spreadsheet we're given.

*   We'll have a record of what we did
    (something that clicking in a spreadsheet won't give us).

> ## FIXME {.challenge}
>
> FIXME
