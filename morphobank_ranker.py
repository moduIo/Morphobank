####
# Features are read from CSV and ranked in order of best fit.
# ---
# COMMAND LINE ARGUMENTS:
# sys.argv[1] := Path location to feature CSV file
# sys.argv[2] := A comma separated list of ranges to rank, if '' the entire feature file is ranked
#
# Example Usage: 
# python3 morphobank_ranker.py 'features.txt' '267-272, 4531-4541'
####
import sys
import csv

####
# Main
####
candidates = {}  # Dict keyed by feature ID

with open(sys.argv[1], newline='') as feature_file:
	feature_reader = csv.reader(feature_file, delimiter=',', quotechar='|')

	# Rank entire feature file
	if sys.argv[2] == '':
		
		# Rank each feature vector by simple summation
		for row in feature_reader:
			total = float(row[2]) + float(row[3]) + float(row[4])

			# Only add the most promising features to be checked
			if total > 1.5 and float(row[2]) > .1:
				candidates[row[0]] = [total, row[1]]

	# Only rank features within the range specified
	else:

		# Parse the argument into ranges for each matrix
		ranges = sys.argv[2].split(',')

		for row in feature_reader:
			cols = row[0].split(' x ')
			total = float(row[2]) + float(row[3]) + float(row[4])

			# Check if both columns are in range
			if int(ranges[0].split('-')[0]) <= int(cols[0].split('_')[1]) <= int(ranges[0].split('-')[1]) and int(ranges[1].split('-')[0]) <= int(cols[1].split('_')[1]) <= int(ranges[1].split('-')[1]):
				candidates[row[0]] = [total, row[1]]

# Write candidates to file
f = open('candidates.txt', 'w+')

for feature in sorted(candidates):
	f.write(feature + ': ' + str(candidates[feature]) + '\n')

f.close()