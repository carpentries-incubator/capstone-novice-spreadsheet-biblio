# count-lines.py
# Count how many lines there are in the spreadsheet
import sys

filename = sys.argv[1]
count = 0

with open(filename, 'r') as reader:
    for line in reader:
        count += 1

print count
