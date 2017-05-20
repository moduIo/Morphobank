####
# Data is parsed from Morphobank files into Column objects which represent the column schema without any instance data.
# Next features are extracted from the data by comparing column trigrams from different matrices.
# The features are then stored in a CSV file for future processing.
#
# ---
# COMMAND LINE ARGUMENTS:
# sys.argv[1] := a CSV list of paths to Morphobank files
# sys.argv[2] := 'printCols' outputs the results of parsing
# sys.argv[3] := 'printFeatures' outputs the results of feature generation
# sys.argv[4] := a valid filepath to write the features in CSV format to
#
# Example Usage: 
# python3 morphobank_parser.py 'Morphobank/P104mbank_X425_2-2-2017_84_no_notes.txt, Morphobank/P157mbank_X430_2-2-2017_82_no_notes.txt' 'printCols' 'printFeatures' 'features.txt'
####
import sys
import re
import codecs
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
		self.labels_trigram = list(trigrams(str(self.labels)))
		self.states_trigram = list(trigrams(" ".join(self.states)))

###
# Feature class has attribtues for features generated by comparing trigrams
# of Column instances from different source matrices
###
class Feature:

	####
	# Constructor
	# ---
	# INPUT:
	# ID := ID string of the form 'columnSourceA' x 'columnSourceB'
	# jaccard_label_similarity := Computed label similarity, a float
	# jaccard_state_similarity := Computed state similarity, a float
	####
	def __init__(self, ID, jaccard_label_similarity, jaccard_state_similarity):
		self.ID = ID
		self.jaccard_label_similarity = jaccard_label_similarity
		self.jaccard_state_similarity = jaccard_state_similarity

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
# Function generates Feature() instances by comparing fields from Column()
# instances which are from different matrices.
# ---
# INPUT:
# columns := a dict of Column() instances
#
# RETURNS:
# A list of Feature() instances
####
def generateFeatures(columns):
	features = []   # List of Feature() instances
	generated = []  # List of matrices which have already generated features, format is (A, B)

	# Iterate over each pair of distinct matrices
	for A in sorted(columns):
		for B in sorted(columns):

			# Do not compute metrics between the same matrix
			if A == B:
				continue

			# Do not compute the same data twice
			if '(' + A + ' x ' + B + ')' in generated or '(' + B + ' x ' + A + ')' in generated:
				continue

			# Compute metrics over each pair of columns in the matrices
			for a in columns[A]:
				for b in columns[B]:

					# Create ID for feature
					ID = a.source + ' x ' + b.source
					feature = Feature(ID, jaccardSimilarity(a.labels_trigram, b.labels_trigram), jaccardSimilarity(a.states_trigram, b.states_trigram))
					features.append(feature)

			generated.append('(' + A + ' x ' + B + ')')

	return features

###
# Function computes the Jaccard Similarity between two sets of trigrams.
# The similarity is simply the cardinality of the intersection divided by the cardinality of the union.
# ---
# INPUT:
# A, B := sets of character trigrams
#
# RETURNS:
# The computed Jaccard Similarity
###
def jaccardSimilarity(A, B):
	union = set().union(A, B)
	intersection = set(A).intersection(B)

	return len(intersection) / len(union)

####
# Main method stores parsed data and trigrams into column objects.
# Features are then generated and output in CSV format to the given filepath.
# Data is output if required.
####
sources = []  # List of source matrices
columns = {}  # Dict of Column() lists, key is the source name
datas = []    # List of parsed data from each source

# Parse each input file
for f in sys.argv[1].split(', '):
	datas.append(parse(f))
	sources.append(f.split('_')[0].replace('Morphobank/', ''))

# Store data into Column() objects
for i, data in enumerate(datas):
	data_columns = []

	for j, state, in enumerate(data['states']):
		column = Column(sources[i] + str(j + 1), data['labels'][j], state)
		data_columns.append(column)
		
	columns[sources[i]] = data_columns

# Print data
if sys.argv[2] == 'printCols':
	print("\nPrinting columns...\n")

	for source in sorted(columns):
		for column in columns[source]:
			print('ID: ' + str(column.source))
			print('Label: ' + str(column.labels))
			print('States: ' + str(column.states))
			print('Label Trigrams: ') 
			print(column.labels_trigram)
			print('\nState Trigrams: ' )
			print(column.states_trigram)
			print('---\n')

# Generate features
print('\nGenerating features...\n')
features = generateFeatures(columns)

if sys.argv[3] == 'printFeatures':
	for feature in features:
		print('ID: ' + feature.ID)
		print('Jaccard Label Similarity: ' + str(feature.jaccard_label_similarity))
		print('Jaccard State Similarity: ' + str(feature.jaccard_state_similarity) + '\n---\n')

# Write features to CSV file
with open(sys.argv[4], 'w+') as f: 
	for feature in features:
		f.write(str(feature.jaccard_label_similarity) + ', ' + str(feature.jaccard_state_similarity) + '\n')