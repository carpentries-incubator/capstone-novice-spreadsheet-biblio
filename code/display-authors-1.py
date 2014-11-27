# display-authors-1.py
# Print (key, author) pairs.

import sys
import csv

raw = open(sys.argv[1], 'r')
reader = csv.reader(raw);
for line in reader:
    key, authors = line[0], line[3]
    for auth in authors.split(';'):
        print key, auth
reader.close()
