import csv
import json
data = []
with open("zips.json", "r") as infile:
    for line in infile:
	    data.append(json.loads(line))
with open("zips.csv", "w") as outfile:
    writer = csv.writer(outfile)
    col_order = [1, 2, 3, 4, 0]
	writer.writerow(["city", "loc", "pop", "state", "zip"])
	for row in data:
	    writer.writerow([list(row.values())[i] for i in col_order])