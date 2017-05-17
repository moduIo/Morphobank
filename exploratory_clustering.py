####
# Runs clustering algorithms on features parsed from Morphobank examples.
# Implements: K-means
# ---
# COMMAND LINE ARGUMENTS:
# sys.argv[1] := a CSV list of paths to Morphobank files
#
# Ex: python3 exploratory_clustering.py 'Morphobank/P104mbank_X425_2-2-2017_84_no_notes.txt, Morphobank/P157mbank_X430_2-2-2017_82_no_notes.txt'
####
import sys
import re
import codecs
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

####
# Column class has attributes for parsed data
####
class Column:

	# Constructor
	def __init__(self):
		return

####
# Function parses from Morphobank file
# ---
# RETURNS: 
# A dict of parsed data with keys {'taxa', 'labels', 'states', 'matrices'}
####
def parse(path):
	data = {}      # Dictionary of data
	taxa = []      # List of taxa (rows)
	labels = []    # List of labels
	states = []    # List of states
	matrices = []  # List of matrices

	print('======\n\nParsing ' + path + '...\n')

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

	print(taxa)

	# Get CHARACTERS data
	chars_data = contents[1].split('\n')[5:]  # Skip preamble
	headers = ''.join(chars_data).split('\t;')  # Parse headers (labels, states, matrices)

	# Preprocess header strings
	char_labels = headers[0].split('\t')
	state_labels = headers[1].replace('STATELABELS', '').split(',')
	matrix = headers[2]

	# Parse CHARLABELS data (labels)
	print('\n---\n\tParsing CHARLABELS data...')

	for label in char_labels:
		cleaned = re.sub('\[[0-9]*\]', '', label).replace("'", '')

		if cleaned != '':
			labels.append(cleaned[2:])

	print(labels)

	# Parse STATELABELS data (states)
	print('\n---\n\tParsing STATELABELS data...')

	for state in state_labels:
		print(re.sub('[0-9]*\t' ,'', state))

####
# Main
####
columns = []  # List of columns

for f in sys.argv[1].split(', '):
	parse(f)
