# count-lines.py
# Count how many lines there are in the spreadsheet
import sys

filename = sys.argv[1]
reader = open(filename, 'r')
count = 0
for line in reader:
    count += 1
reader.close()
print count
