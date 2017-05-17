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
# Function parses from Morphobank file
####
def parse(path):

	print('---\n\nParsing ' + path + '...\n')
	# Get relevant data from file
	with codecs.open(path, "r", encoding='utf-8', errors='ignore') as f:
	    data = f.read().split('BEGIN')[1:3]

 	# Get TAXA data
	taxa_data = data[0].split('\n')[2:]  # Skip preamble
	taxa = []

	# Parse the labels
	print('Parsing TAXA data...\n')

	for line in taxa_data:
		if "\t\t" in line:
			taxa.append(line.replace('\t\t', '').replace('\'', ''))

	print(taxa)

	# Get CHARACTERS data
	chars_data = data[1].split('\n')[5:]  # Skip preamble
	headers = ''.join(chars_data).split('\t;')  # Parse headers
	char_labels = headers[0]
	state_labels = headers[1]
	matrix = headers[2]

	print('---\n\nParsing CHARACTERS data...\n')
	print(state_labels)
	print('\n------------------\n')

####
# Main
####
for f in sys.argv[1].split(', '):
	parse(f)
