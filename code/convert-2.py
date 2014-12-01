# convert-2.py
# Create database of keys and authors.

import sys
import csv

CREATE = 'create table data(key text not null, author text not null);'
INSERT = 'insert into data values("{0}", "{1}");'

print CREATE

raw = open(sys.argv[1], 'r')
reader = csv.reader(raw);
for line in reader:
    key, authors = line[0], line[3]
    for auth in authors.split('; '):
        print INSERT.format(key, auth)
raw.close()
