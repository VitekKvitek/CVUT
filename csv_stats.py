import csv
from collections import Counter
import matplotlib.pyplot as plt


csv_file = ""

sorted_data = Counter()

with open(csv_file, mode="r", newline="") as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    source_data_list = list(csvreader)

for row in source_data_list:
    if row[5] == "1":
        sorted_data[row[6]] += 1

print(sorted_data.values())
print(list(sorted_data))

left_coordinates=[1,2,3,4,5,6,7,8,9,10]
heights = sorted_data.values()
bar_labels = list(sorted_data) # list of elements
plt.bar(left_coordinates,heights,tick_label=bar_labels,width=0.6)
plt.xlabel('orientations')
plt.ylabel('count')
plt.title("TCCPD, white bg only")
plt.grid("on")
plt.show()
