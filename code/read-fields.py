# read-fields.py
# Make sure we can read the fields from a CSV file.

import sys
import csv

with open(sys.argv[1], 'r') as raw:
    reader = csv.reader(raw);
    for line in reader:
        print line

