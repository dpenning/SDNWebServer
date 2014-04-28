import sys

def parse_config(config_file_location):
	nodes = []
	connections = []
	try:
		file_lines = open(config_file_location).readlines()
	except IOError:
		print "Cant find the config file."
		print "\t+ "+config_file_location
		sys.exit()
	check_flag = 	[	"__NODES_LIST__",
						"__CONNECTIONS_LIST__"]
	check_off_flag = [	"__OFF_NODES_LIST__",
						"__OFF_CONNECTIONS_LIST__"]
	node_read = False
	conn_read = False

	for a in file_lines:
	#check Flags
		if check_flag[0] in a:
			node_read = True
			continue
		if check_off_flag[0] in a:
			node_read = False
			continue

		if check_flag[1] in a:
			conn_read = True
			continue
		if check_off_flag[1] in a:
			conn_read = False
			continue
	#check Values
		if node_read:
			print "reading nodes: ",a.strip("\n")
			nodes.append(parse_config_node(a))
			continue
		if conn_read:
			print "reading connections: ",a.strip("\n")
			connections.append(parse_config_connections(a))
			continue
	return nodes,connections
def parse_config_node(line):
	x = line.split("__=__")
	return [pretty_string(x[0]),pretty_string(x[1])]
def parse_config_connections(line):
	global connections
	x = (line.split('__=__'))
	return [pretty_string(x[0]),pretty_string(x[1])]
def pretty_string(line):
	return line.replace(" ","").replace("\t","").replace("\n","")

if __name__ == "__main__":
	parse_config("config.txt")