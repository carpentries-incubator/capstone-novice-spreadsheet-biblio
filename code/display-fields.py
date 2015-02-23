# display-fields.py
# Print the key and all the authors

import sys
import csv

with open(sys.argv[1], 'r') as raw:
    reader = csv.reader(raw);
    for line in reader:
        print line[0], line[3]

