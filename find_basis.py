import json
import networkx as nx
import time
import matplotlib as matplotlib
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


#------------------------------------------------------------------------------
#								Constants
#------------------------------------------------------------------------------

DICTIONARY = 'small_dictionary.json'

#------------------------------------------------------------------------------
#								Functions
#------------------------------------------------------------------------------
def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


def read_dictionary(file):
	start = time.time()
	with open(file) as f:
		data = json.load(f)
	end = time.time()
	print("Dictionary Loaded. (%.4f sec.)" % (end - start))
	return data

def clean_dictionary(rawdata):
	start = time.time()
	data = {}
	for key in rawdata:
		if '*' not in rawdata[key]:
			data[key.lower()] = rawdata[key].lower()

	# for key in data:
	# 	print("Word: " + str(key))
	# 	print("Definition: " + str(data[key]))

	for key in data:
		data[key] = ' '.join([word for word in data[key].split() if '*' not in word])
		data[key] = ''.join([char for char in data[key] if char.isalpha() or char == ' '])
		unlemmatized = data[key].split()
		# data[key] = []
		# for word in unlemmatized:
		# 	if 
	end = time.time()
	print("Dictionary Cleaned. (%.4f sec.)" % (end - start))
	return data

def populate_graph(data, wordnet):
	# wnl = WordNetLemmatizer()
	start = time.time()
	for key in data:
		targets = data[key].split()
		for target in targets:
			# targetStem = st.stem(target)
			try:
				wordnet.add_edge(key, target)
				#Uncomment this print for debugging purposes
				#print("Added edge from " + str(key) + " to " + str(target))
			except:
				print("could not add edge from " + str(key) + " to " + str(targetStem))
	end = time.time()
	print("Graph Populated. (%.4f sec.)" % (end - start))
	return wordnet

def generate_image(fgraph, basis):
	start = time.time()
	pos = nx.layout.spring_layout(fgraph)
	node_sizes = []

	for node in fgraph.nodes:
		if fgraph.degree(node) > 1:
			node_sizes.append(fgraph.degree(node) * 3)
		else:
			node_sizes.append(0)
	edgelist = []
	edgecolors = []
	for s,e in fgraph.edges:
		if fgraph.degree(s) > 1 and fgraph.degree(e) > 1:
			edgelist.append((s,e))
			edgecolors.append(10 * fgraph.degree(e))

	node_colors = []
	for node in fgraph.nodes:
		if node in basis:
			node_colors.append('yellow')
		else:
			node_colors.append('blue')



	#Uncomment this print for debugging purposes
	#print(node_sizes)
	nodes = nx.draw_networkx_nodes(fgraph, pos, node_color=node_colors, node_size = node_sizes)

	# Change 'edgecolor' to edgecolor=edgecolors to switch the edge style (see for loop above)
	edges = nx.draw_networkx_edges(fgraph, pos, arrowstyle='->',   node_size = node_sizes,
								   arrowsize=5, edgelist=edgelist, edge_cmap=plt.cm.Blues, 
								   edgecolor='', width=1)

	end = time.time()
	print("Graph Image Generated. (%.4f sec.)" % (end - start))

	ax = plt.gca()
	ax.set_axis_off()
	plt.show()


def find_basis_words(wordnet):
	# components = nx.strongly_connected_components(wordnet)
	# scc_graph = nx.condensation(wordnet)

	#now we find sinks of the sccgraph
	sink_sccs = nx.attracting_components(wordnet)


	#now we simply choose a node from all sccsinks, and we can generate all definitions
	basis_words = set()
	for scc in sink_sccs:
		basis_words.add(scc.pop())

	return basis_words



#------------------------------------------------------------------------------
#								Main
#------------------------------------------------------------------------------
def main():
	raw_dictionary = read_dictionary(DICTIONARY)
	data = clean_dictionary(raw_dictionary)

	wordnet = nx.DiGraph()
	wordnet.add_nodes_from(data.keys())

	wordnet = populate_graph(data, wordnet)

	basis = find_basis_words(wordnet)

	print(basis)

	generate_image(wordnet, basis)

if __name__ == '__main__':
	main()