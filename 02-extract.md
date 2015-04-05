---
layout: page
title: From a Spreadsheet to a Database
subtitle: Extracting Data
minutes: 10
---
> ## Learning Objectives {.objectives}
>
> * Explain why we call `csv.reader` a "wrapper".
> * Write a short Python program to extract data from a CSV file.
> * Explain the pitfalls of parsing data formats like CSV using string splitting.
> * Explain why string splitting is nevertheless an acceptable approach for extracting authors' names from this data.

The first step is to turn the rows of the spreadsheet into (key, author) pairs.
Let's start by making sure that Python can read the spreadsheet properly:

~~~ {.python}
# count-lines.py
# Count how many lines there are in the spreadsheet
import sys

filename = sys.argv[1]
count = 0

with open(filename, 'r') as reader:
    for line in reader:
        count += 1

print count
~~~

This should look familiar by now:
the filename is given as the first command-line argument (`sys.argv[1]`),
so we open that file and use a `for` loop to read it line by line.
Each time the loop executes,
it adds 1 to a variable called `count`;
when the loop finishes,
we close the file and print the count.

We can run this program like this:

~~~ {.input}
$ python code/count-lines.py data/bibliography.csv
~~~

Sure enough, its output is:

~~~ {.output}
2937
~~~

so we know that Python is reading all of the rows.

The next step is to break each line into fields
so that we can get each entry's key and authors.
The fields are separated by commas,
so we could try using `str.split`.
This won't work,
though,
because authors' names also contain commas (since they are formatted as "last, first").

What we can do instead is ask our favorite search engine for help.
Sure enough,
a search for "python csv" turns up
[a library called `csv`](https://docs.python.org/2/library/csv.html),
which is part of the standard Python distribution.
Its documentation includes a few examples,
and after a couple of experiments,
we come up with this:

~~~ {.python
# read-fields.py
# Make sure we can read the fields from a CSV file.

import sys
import csv

with open(sys.argv[1], 'r') as raw:
    reader = csv.reader(raw);
    for line in reader:
        print line

~~~

This program starts by opening the bibliography file
(again, we'll pass its name as the first command-line argument).
It then calls `csv.reader` to create a wrapper around the file.
When the basic file object created by `open` reads a line at a time,
the wrapper created by `csv.reader` breaks that line into fields at the right places.
It knows how to handle commas embedded in fields,
special characters,
and a bunch of other things that we don't want to have to worry about.

To check that it's working correctly,
we just print out each line after it has been processed by the CSV reader.
Its first few lines of output are:

~~~ {.input}
$ python code/read-fields.py data/bibliography.csv | head -5
~~~
~~~ {.output}
['8SW85SQM', 'journalArticle', '2013', 'McClelland, James L', 'Incorporating Rapid Neocortical Learning of New Schema-Consistent Information Into Complementary Learning Systems Theory.', 'J Exp Psychol Gen', '', '1939-2222', '', 'http://www.biomedsearch.com/nih/Incorporating-Rapid-Neocortical-Learning-New/23978185.html', '', '', '', '', '', '', '', '', '']
['85QV9X5F', 'journalArticle', '1995', "McClelland, J. L.; McNaughton, B. L.; O'Reilly, R. C.", 'Why There are Complementary Learning Systems in the Hippocampus and Neocortex: Insights from the Successes and Failures of Connectionist Models of Learning and Memory', 'Psychological Review', '', '', '', '', '', '', '', '', '', '', '', '', '']
['Z4X6DT6N', 'journalArticle', '1990', 'Ratcliff, R.', 'Connectionist models of recognition memory: constraints imposed by learning and forgetting functions.', 'Psychological review', '', '0033-295X', '', 'http://view.ncbi.nlm.nih.gov/pubmed/2186426', '', '', '', '', '', '', '', '', '']
['F5DGU3Q4', 'bookSection', '1989', 'McCloskey, M.; Cohen, N. J.', 'Catastrophic Interference in Connectionist Networks: The Sequential Learning Problem', 'The Psychology of Learning and Motivation, Vol. 24', '', '', '', '', '', '', '', '', '', '', '', '', '']
['PNGQMCP5', 'conferencePaper', '2006', 'Bucilu\xc7\x8e, Cristian; Caruana, Rich; Niculescu-Mizil, Alexandru', 'Model compression', 'Proceedings of the 12th ACM SIGKDD international conference on Knowledge discovery and data mining', '', '', '', '', '', '', '', '', '', '', '', '', '']
~~~

(Notice that we run the program's output through `head` to only display the first few lines
rather than scrolling back through its output.)
This is exactly what we need:
the key is in the first element of each list,
and the authors are all together in the fourth.
Let's modify the program to print out just those two fields:

~~~ {.python}
# display-fields.py
# Print the key and all the authors

import sys
import csv

with open(sys.argv[1], 'r') as raw:
    reader = csv.reader(raw);
    for line in reader:
        print line[0], line[3]

~~~

Its output is:

~~~ {.output}
8SW85SQM McClelland, James L
85QV9X5F McClelland, J. L.; McNaughton, B. L.; O'Reilly, R. C.
Z4X6DT6N Ratcliff, R.
F5DGU3Q4 McCloskey, M.; Cohen, N. J.
PNGQMCP5 Buciluǎ, Cristian; Caruana, Rich; Niculescu-Mizil, Alexandru
~~~

The last step is to turn lines with multiple authors into multiple lines,
each with a single author.
This is the right time to use `str.split`:
the authors' names are separated by semi-colons,
so we can break each list of authors on those
and use another loop to print the results one by one:

~~~ {.input}
$ python code/display-authors-1.py data/bibliography.csv | head -10
~~~
~~~ {.output}
8SW85SQM McClelland, James L
85QV9X5F McClelland, J. L.
85QV9X5F  McNaughton, B. L.
85QV9X5F  O'Reilly, R. C.
Z4X6DT6N Ratcliff, R.
F5DGU3Q4 McCloskey, M.
F5DGU3Q4  Cohen, N. J.
PNGQMCP5 Buciluǎ, Cristian
PNGQMCP5  Caruana, Rich
PNGQMCP5  Niculescu-Mizil, Alexandru
~~~

That's close to what we want, but not quite right:
since authors' names are actually separated by a semi-colon and a space,
and we're only splitting on semi-colons,
the second and subsequent name on each line comes out with an unwanted space at the front.
What happens if we try to split on a semi-colon plus a space?

~~~ {.python}
# display-authors-2.py
# Print (key, author) pairs.

import sys
import csv

with open(sys.argv[1], 'r') as raw:
    reader = csv.reader(raw);
    for line in reader:
        key, authors = line[0], line[3]
        for auth in authors.split('; '): # semi-colon plus space instead of semi-colon
            print key, auth

~~~
~~~ {.output}
8SW85SQM McClelland, James L
85QV9X5F McClelland, J. L.
85QV9X5F McNaughton, B. L.
85QV9X5F O'Reilly, R. C.
Z4X6DT6N Ratcliff, R.
F5DGU3Q4 McCloskey, M.
F5DGU3Q4 Cohen, N. J.
PNGQMCP5 Buciluǎ, Cristian
PNGQMCP5 Caruana, Rich
PNGQMCP5 Niculescu-Mizil, Alexandru
~~~

And that's that:
the first step of our data extraction is done.
Since we've achieved something useful,
we save it for posterity:

~~~ {.input}
$ git init .
~~~
~~~ {.output}
Initialized empty Git repository in /Users/aturing/lessons/capstone-novice-spreadsheet-biblio/.git
~~~
~~~ {.input}
$ git add -A
$ git status
~~~
~~~ {.output}
On branch master

Initial commit

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

  new file:   code/count-lines.py
  new file:   code/display-authors-1.py
  new file:   code/display-authors-2.py
  new file:   code/display-fields.py
  new file:   code/read-fields.py
  new file:   data/bibliography.csv
~~~
~~~ {.input}
$ git commit -m "Extracting (key, author) pairs from bibliography"
~~~
~~~ {.output}
[master (root-commit) 9db78ed] Extracting (key, author) pairsfrom bibliography
 6 files changed, 2996 insertions(+)
 create mode 100644 code/count-lines.py
 create mode 100644 code/display-authors-1.py
 create mode 100644 code/display-authors-2.py
 create mode 100644 code/display-fields.py
 create mode 100644 code/read-fields.py
 create mode 100644 data/bibliography.csv
~~~

> ## Checking Assumptions {.challenge}
>
> You suspect that a handful of authors' names are separated only by a semi-colon
> rather than by a semi-colon and space.
> What Unix shell command or commands could you use to check for this?

> ## Safer Splitting {.challenge}
>
> Suppose you find that some authors' names are separated only by a semi-colon
> rather than by a semi-colon and a space.
> Modify the program so that it splits the author field on semi-colons,
> then strips unwanted spaces from individual authors' names while printing.
