# convert-1.py
# Create SQL statements to put (key, author) pairs in a database.

import sys
import csv

INSERT = "insert into data values('{0}', '{1}');"

raw = open(sys.argv[1], 'r')
reader = csv.reader(raw);
for line in reader:
    key, authors = line[0], line[3]
    for auth in authors.split('; '):
        print INSERT.format(key, auth)
raw.close()
