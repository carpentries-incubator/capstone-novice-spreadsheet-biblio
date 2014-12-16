---
layout: page
title: Lesson Title
subtitle: Reference
---
## [Introduction](01-intro.html)

*   Data in a database is usually easier to query than data in a spreadsheet.

*   Writing tools to extract and reformat data
    allows us to re-use our work
    and gives us a record of what we did.

*   Tool-based data extraction and reformatting is more likely to be correct
    than manual extraction and reformatting.

## [Extracting Data](02-extract.html)

*   Search for a library to solve a problem before writing code to solve it.

*   Always use the `csv` library to handle CSV data.

*   Use pipelines of command-line tools to do spot checks
    of data's correctness
    when extracting and reformatting.

*   Put all work under version control.

## [Storing Data in a Database](03-db.html)

*   A program can print `create` and `insert` statements
    to generate a simple database
    instead of working with the database programmatically,
    but this should only be done in very simple cases.

*   Normalized data is much easier to work with than denormalized data.

*   Heuristically normalized data is only ever approximately correct.

*   Record the heuristics used,
    how they were implemented,
    and what effect they had on data
    so that analysis can be repeated later.

## Glossary

normalized data
:   Data that contains no redundancy,
    i.e.,
    each fact is represented once and in one place.

heuristic
:   A guideline for solving a problem that is usually, but not always, correct.
