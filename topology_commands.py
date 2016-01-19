import httplib2
import json

def print_graph(g):
	for a in g:
		print str(a).replace("[","").replace("]","").replace(",","")
def build_slice(n1,n2,nodes,connections):
	#build graph from nodes and connetions

	if n1 in nodes:
		n_1 = nodes.index(n1)
	else:
		return "bad search not matching nodes"
	if n2 in nodes:
		n_2 = nodes.index(n2)
	else:
		return "bad search not matching nodes"


	graph = []
	node_ids = []
	for a in nodes:
		l = []
		node_ids.append(a[0])
		for b in nodes:
			l.append(0)
		graph.append(l)
	for a in connections:

		if a[0] in node_ids:
			index_1 = node_ids.index(a[0])
		else:
			return "connection not matcing nodes"

		if a[1] in node_ids:
			index_2 = node_ids.index(a[1])
		else:
			return "connection not matcing nodes"
		graph[index_1][index_2] = 1
		graph[index_2][index_1] = 1

	#breadth first search to find least connections
	possible_graphs = [[n_1]]
	path_not_found = True
	correct_path = []
	while path_not_found:
		next_possible_graphs = []
		for a in possible_graphs:
			for b in xrange(len(graph[a[-1]])):
				if graph[a[-1]][b] != 0:
					x = a + [b]
					if b == n_2:
						if path_not_found:
							path_not_found = False
							correct_path = x
					next_possible_graphs.append(x)
		possible_graphs = next_possible_graphs
	#build the html page for the output
	return correct_path
def build_slice_command(name,node,ingress,priority,ethertype,vlanid,nwsrc,actions):
	global daylight_ip
	global daylight_port

	input_flow = {	
		"installInHw":"true", 
		"name":str(name), 
		"node":	{
					"id":str(node), 
					"type":"OF"
				},
		"ingressPort":str(ingress), 
		"priority":str(priority), 
		"etherType":str(ethertype), 
		"vlanId":str(vlanid), # ingress vlan
		"nwSrc":str(nwsrc), 
		"actions":actions,
	}

	daylight_id = ''
	daylight_port = ''

	u = ""#username for the daylight controller
	p = ""#pass for the daylight controller

	url = 'http://' + str(daylight_ip) + ":" + str(daylight_port) + \
	'/controller/nb/v2/flowprogrammer/default/node/OF/' + \
	str(input_flow["node"]["id"]) + "/staticFlow/" + str(input_flow["name"]) 

	h = httplib2.Http(".cache")
	h.add_credentials(u, p)
	resp, content = h.request(url,"PUT", body=str(json.dumps(input_flow)), headers={'content-type':'application/json'} )

def build_base_rules(daylight_ip,
	daylight_port,
	user,
	passw,
	nodes,
	connections,
	hosts):

	h = httplib2.Http(".cache")
	h.add_credentials(u, p)


	for a in nodes:

		######### Change For Production Network #########
		if a[1] == "vinni":
			input_flow = {
				"name":"normal_37",
				"node":a[0],
				"ingressPort":'37',
				"priority":"100",
				"etherType":"0x0800",
				"actions":["HW_PATH"]
			}
			url = 'http://' + str(daylight_ip) + ":" + str(daylight_port) + '/controller/nb/v2/flowprogrammer/default/node/OF/' + str(input_flow["node"]) + "/staticFlow/" + str(input_flow["name"]) 
			resp, content = h.request(url,"PUT", body=str(json.dumps(input_flow)), headers={'content-type':'application/json'} )

		######## /Change For Production Network #########


		input_flow = {
			"name":"arp",
			"node":a[0],
			"priority":"100",
			"etherType":"0x0806",
			"actions":["HW_PATH"]
		}
		url = 'http://' + str(daylight_ip) + ":" + str(daylight_port) + '/controller/nb/v2/flowprogrammer/default/node/OF/' + str(input_flow["node"]) + "/staticFlow/" + str(input_flow["name"]) 
		resp, content = h.request(url,"PUT", body=str(json.dumps(input_flow)), headers={'content-type':'application/json'} )
		input_flow = {
				"name":"dhcp",
				"node":a[0],
				"priority":"100",
				"etherType":"0x0800",
				"protocol":"UDP", # IP protocol
				"tpDst":"67", # protocol port
				"actions":["HW_PATH"]
			}
		url = 'http://' + str(daylight_ip) + ":" + str(daylight_port) + '/controller/nb/v2/flowprogrammer/default/node/OF/' + str(input_flow["node"]) + "/staticFlow/" + str(input_flow["name"]) 
		resp, content = h.request(url,"PUT", body=str(json.dumps(input_flow)), headers={'content-type':'application/json'} )
		print "-----------"
		print content
		print "-----------"
		for b in connections:
			if a[0] == b["edge"]["tailNodeConnector"]["node"]["id"]:
				input_flow = {
					"name":"normal_"+b["edge"]["tailNodeConnector"]["id"],
					"node":b["edge"]["tailNodeConnector"]["node"]["id"],
					"ingressPort":b["edge"]["tailNodeConnector"]["id"],
					"priority":"100",
					"etherType":"0x0800",
					"actions":["HW_PATH"]
				}
				url = 'http://' + str(daylight_ip) + ":" + str(daylight_port) + '/controller/nb/v2/flowprogrammer/default/node/OF/' + str(input_flow["node"]) + "/staticFlow/" + str(input_flow["name"]) 
				resp, content = h.request(url,"PUT", body=str(json.dumps(input_flow)), headers={'content-type':'application/json'} )
			if a[0] == b["edge"]["headNodeConnector"]["node"]["id"]:
				input_flow = {
					"name":"normal_"+b["edge"]["headNodeConnector"]["id"],
					"node":b["edge"]["headNodeConnector"]["node"]["id"],
					"ingressPort":b["edge"]["headNodeConnector"]["id"],
					"priority":"100",
					"etherType":"0x0800",
					"actions":["HW_PATH"]
				}
				url = 'http://' + str(daylight_ip) + ":" + str(daylight_port) + '/controller/nb/v2/flowprogrammer/default/node/OF/' + str(input_flow["node"]) + "/staticFlow/" + str(input_flow["name"]) 
				resp, content = h.request(url,"PUT", body=str(json.dumps(input_flow)), headers={'content-type':'application/json'} )




if __name__ == "__main__":
	import config_parser
	nodes,connections = config_parser.parse_config("config.txt")
	x = build_slice(nodes[0],nodes[2],nodes,connections)
	print x
	names = [nodes[a][1] for a in x]
	print names
