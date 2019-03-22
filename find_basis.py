import json
import networkx as nx
import time
import matplotlib as matplotlib
import matplotlib.pyplot as plt

DICTIONARY = 'small_dictionary.json'

def read_dictionary(file):
	start = time.time()
	with open(file) as f:
		data = json.load(f)
	end = time.time()
	print("Dictionary Loaded (" + str(end - start) + " sec.)")
	return data

def clean_dictionary(rawdata):
	data = {}
	for key in rawdata:
		if '*' not in rawdata[key]:
			data[key.lower()] = rawdata[key].lower()

	# for key in data:
	# 	print("Word: " + str(key))
	# 	print("Definition: " + str(data[key]))

	for key in data:
		data[key] = ' '.join([word for word in data[key].split() if '*' not in word])
		data[key] = ''.join([char for char in data[key] if char.isalpha() or char == ' ']) # If you look closely, you can see what it's doing.
		data[key] = data[key].split()

	return data

def populate_graph(data, wordnet):
	start_time = time.time()
	for key in data:
		targets = data[key]
		for target in targets:
			try:
				wordnet.add_edge(key, target)
				print("Added edge from " + str(key) + " to " + str(target))
			except:
				print("could not add edge from " + str(key) + " to " + str(target))
	end_time = time.time()
	print("Graph populated. (" + str(end_time - start_time) + " sec.)")
	return wordnet

def generate_image(fgraph):
	pos = nx.layout.spring_layout(fgraph)
	node_sizes = []
	for node in fgraph.nodes:
		if fgraph.degree(node) > 1:
			node_sizes.append(fgraph.degree(node) * 3)
		else:
			node_sizes.append(0)

	# arrow_sizes = []
	# for s,e in fgraph.edges:
	# 	if fgraph.degree(s) > 1 and fgraph.degree(e) > 1:
	# 		arrow_sizes.append(1)
	# 	else:
	# 		arrow_sizes.append(0)
	edgelist = []
	for s,e in fgraph.edges:
		if fgraph.degree(s) > 1 and fgraph.degree(e) > 1:
			edgelist.append((s,e))

	# node_sizes = [3 * fgraph.degree(node) for node in fgraph.nodes if fgraph.degree(node) > 1]
	print(node_sizes)
	nodes = nx.draw_networkx_nodes(fgraph, pos, node_color='blue', node_size = node_sizes)
	edges = nx.draw_networkx_edges(fgraph, pos, arrowstyle='->',   node_size = node_sizes,
									arrowsize=5, edgelist = edgelist, edge_cmap=plt.cm.Blues, width=1)

	plt.show()

def main():
	raw_dictionary = read_dictionary(DICTIONARY)
	data = clean_dictionary(raw_dictionary)

	wordnet = nx.DiGraph()
	wordnet.add_nodes_from(data.keys())

	wordnet = populate_graph(data, wordnet)

	generate_image(wordnet)

if __name__ == '__main__':
	main()