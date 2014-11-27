# display-fields.py
# Print the key and all the authors

import sys
import csv

raw = open(sys.argv[1], 'r')
reader = csv.reader(raw);
for line in reader:
    print line[0], line[3]
reader.close()
