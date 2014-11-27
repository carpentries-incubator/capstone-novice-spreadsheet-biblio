# read-fields.py
# Make sure we can read the fields from a CSV file.

import sys
import csv

raw = open(sys.argv[1], 'r')
reader = csv.reader(raw);
for line in reader:
    print line
reader.close()
