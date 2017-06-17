####
# Features are read from CSV and ranked in order of best fit.
# ---
#
# Example Usage: 
# python3 morphobank_ranker.py 'features.txt'
####
import sys
import csv

####
# Main
####
candidates = {}  # Dict keyed by feature ID

with open(sys.argv[1], newline='') as feature_file:
	feature_reader = csv.reader(feature_file, delimiter=',', quotechar='|')

	# Rank each feature vector by simple summation
	for row in feature_reader:
		total = float(row[1]) + float(row[2]) + float(row[3])

		# Only add the most promising features to be checked
		if total > 1.5 and float(row[1]) > .1:
			candidates[row[0]] = total

print(len(candidates))

# Write candidates to file
f = open('candidates.txt', 'w+')

for feature in sorted(candidates):
	f.write(feature + ': ' + str(candidates[feature]) + '\n')

f.close()