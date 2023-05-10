import glob
import os

list_of_files = glob.glob('BLAST/*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
a = open(latest_file)
text = ''
for i in range(20):
    x = a.readline()
    text = text + x + '\n'

print(text)