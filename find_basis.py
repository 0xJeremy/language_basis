import json
import networkx as nx
import time

DICTIONARY = 'small_dictionary.json'

def read_dictionary(file):
	start = time.time()
	with open(file) as f:
		data = json.load(f)
	end = time.time()
	print("Dictionary Loaded (" + str(end - start) + " sec.)")
	return data

def main():
	rawdata = read_dictionary(DICTIONARY)
	data = {}
	for key in rawdata:
		if '*' not in rawdata[key]:
			data[key.lower()] = rawdata[key].lower()

	# for key in data:
	# 	if '*' in data[key]:
	# 		data.remove(key)
	# 		continue
	# 	data[key] = data[key].strip()
	# 	print("Word: " + str(key))
	# 	print("Definition: " + str(data[key]))

	for key in data:
		data[key] = ' '.join([word for word in data[key].split() if '*' not in word])
		data[key] = ''.join([char for char in data[key] if char.isalpha() or char == ' ']) # If you look closely, you can see what it's doing.
		data[key] = data[key].split()

	wordnet = nx.DiGraph()
	wordnet.add_nodes_from(data.keys())
	# wordnet.add_node(1)
	print(wordnet.nodes)

	print("Added word nodes to graph.")

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

	print(wordnet.edges)


if __name__ == '__main__':
	main()