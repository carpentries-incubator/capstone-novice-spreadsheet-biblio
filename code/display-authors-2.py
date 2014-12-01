# display-authors-2.py
# Print (key, author) pairs.

import sys
import csv

raw = open(sys.argv[1], 'r')
reader = csv.reader(raw);
for line in reader:
    key, authors = line[0], line[3]
    for auth in authors.split('; '): # semi-colon plus space instead of semi-colon
        print key, auth
raw.close()
