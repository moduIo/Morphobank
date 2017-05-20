####
# Runs clustering algorithms on features parsed from Morphobank examples.
# Data is parsed into Column objects which represent the column schema without any instance data.
# Next features are extracted from the data.
#
# Implements: K-means
# ---
# COMMAND LINE ARGUMENTS:
# sys.argv[1] := a CSV list of paths to Morphobank files
# sys.argv[2] := 'printCols' outputs the results of parsing
#
# Example Usage: 
# python3 exploratory_clustering.py 'Morphobank/P104mbank_X425_2-2-2017_84_no_notes.txt, Morphobank/P157mbank_X430_2-2-2017_82_no_notes.txt' 'printCols'
####
import sys
import re
import codecs
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import nltk
from nltk import word_tokenize
from nltk.util import trigrams

####
# Column class has attributes for parsed data
####
class Column:

	####
	# Constructor computes trigrams of labels and states
	# ---
	# INPUT: 
	# source := Source matrix name
	# labels := Label name
	# states := List of states
	####
	def __init__(self, source, labels, states):
		self.source = source
		self.labels = labels
		self.states = states
		self.labels_trigram = trigrams(str(self.labels))
		self.states_trigram = trigrams(" ".join(self.states))

###
# Sample class has attributes for (x, y) training data.
###
class Sample:

	####
	# Constructor
	####
	def __init__(self, columns):
		self.Greeting = Name + "!"

####
# Function parses from Morphobank file
# ---
# RETURNS: 
# A dict of parsed data with keys {'taxa', 'labels', 'states', 'matrices'}
####
def parse(path):
	taxa = []      # List of taxa (rows)
	labels = []    # List of labels
	states = []    # List of states
	matrices = []  # List of matrices

	# Dictionary of data
	data = {'taxa': taxa, 
			'labels': labels, 
			'states': states, 
			'matrices': matrices}

	print('======\n\nParsing ' + path + '...')

	# Get relevant data from file
	with codecs.open(path, "r", encoding='utf-8', errors='ignore') as f:
	    contents = f.read().split('BEGIN')[1:3]

 	# Get TAXA data
	taxa_data = contents[0].split('\n')[2:]  # Skip preamble

	# Parse the labels
	print('\tParsing TAXA data...')

	for line in taxa_data:
		if "\t\t" in line:
			taxa.append(str(line.replace('\t\t', '').replace('\'', '')))

	# Get CHARACTERS data
	chars_data = contents[1].split('\n')[5:]  # Skip preamble
	headers = ''.join(chars_data).split('\t;')  # Parse headers (labels, states, matrices)

	# Preprocess header strings
	char_labels = headers[0].split('\t')
	state_labels = headers[1].replace('STATELABELS', '').split('\t\t,')
	matrix = headers[2]

	# Parse CHARLABELS data (labels)
	print('\tParsing CHARLABELS data...')

	for label in char_labels:
		cleaned = re.sub('\[[0-9]*\]', '', label).replace("'", '')

		if cleaned != '':
			labels.append(cleaned[2:])

	# Parse STATELABELS data (states)
	print('\tParsing STATELABELS data...')

	for state in state_labels:

		values = []  # Values that current label can assume
		cleaned = re.sub('[0-9]*\t' ,'', state).split("'")

		# Iterate over each substring
		for entry in cleaned:
			if entry != '':
				values.append(entry)

		states.append(values)

	return data

####
# Main method stores parsed data and trigrams into column objects.
# Data is output if required.
####
sources = []  # List of source matrices
columns = []  # List of Column()
datas = []    # List of parsed data

# Parse each input file
for f in sys.argv[1].split(', '):
	datas.append(parse(f))
	sources.append(f.split('_')[0].replace('Morphobank/', ''))

# Store data into Column() objects
for i, data in enumerate(datas):
	for j, state, in enumerate(data['states']):
		column = Column(sources[i], data['labels'][j], state)
		columns.append(column)

# Print data
if sys.argv[2] == 'printCols':
	print("\nPrinting columns...\n")

	for i, column in enumerate(columns):
		print('ID: ' + str(column.source) + ' ' + str(i + 1))
		print('Label: ' + str(column.labels))
		print('States: ' + str(column.states))
		print('Label Trigrams: ') 
		print(list(column.labels_trigram))
		print('\nState Trigrams: ' )
		print(list(column.states_trigram))
		print('---\n')
