---
title: "Introduction"
teaching: 20
exercises: 10
questions:
- "How do we design lessons?"
objectives:
- "Explore the difficulties of working with someone else's spreadsheet."
- "Explore the advantages of a quickly made database to answer research questions."
keypoints:
- "Spreadsheets are inflexible and can present challenges when needing to answer novel questions."
- "It is easier to load data into a database than one might think."
---

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


## Plan for today's lesson

1. Load csv data into a sqlite database using the `sqlite3` command line client.
2. Write a python program 

BBS FIXME



This might seem like a lot of work to answer two questions,
but for anything more than a half-dozen rows,
it will save us a lot of time:

*   Once the data is in a database,
    it will be easy to ask and answer many other questions.
*   We'll be able to re-use our tools on the next spreadsheet we're given.
*   We'll have a record of what we did
    (something that clicking in a spreadsheet won't give us).
*   It's more likely to be correct.

> ## What Are the Odds? 
>
> The spreadsheet contains 2937 rows.
> How accurate does manual transcription have to be
> for us to have a 99% chance of getting the whole analysis right?
> I.e., what error-per-row rate gives us a 0.99 probability
> completing the entire task correctly?
{: .challenge}

> ## Breaking Even {.challenge}
>
> If it takes 10 minutes to write a program to do a task
> that only takes 5 minutes to do by hand,
> the program is only worth writing
> if the task has to be done more than twice.
> Similarly,
> if we only wanted to find out who had co-authored papers with one specific author,
> and we were sure we would never have any other questions
> or need to re-do the analysis,
> manually searching the spreadsheet would probably be faster than
> transcribing the data into a database.
> 
> Choose some task that you currently do by hand.
> Estimate how long it takes you to do it each time,
> how often you do it,
> and how long it would take you to write a program to do the task instead.
> How much time would programming actually save you?
> How sure are you?
{: .challenge}