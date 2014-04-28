import httplib2
import json

def get_graph(ip,port,user,passw):
	nodes_url = "http://" + str(ip) + ":" + str(port) + "/controller/nb/v2/switchmanager/default/nodes/"
	edges_url = "http://" + str(ip) + ":" + str(port) + "/controller/nb/v2/topology/default"
	

	h = httplib2.Http(".Cache")
	h.add_credentials(user,passw)
	resp,content = h.request(nodes_url,"GET")
	c = json.loads(content)
	count = 0
	nodes = []
	for a in c["nodeProperties"]:
		nodes.append([a["node"]["id"],a["properties"]["description"]["value"]])

	resp,content = h.request(edges_url,"GET")
	c = json.loads(content)
	edges = []
	for a in c["edgeProperties"]:
		edges.append(a)

	return nodes,edges
def get_hosts(ip,port,user,passw,nodes):
	hosts_url = "http://" + str(ip) + ":" + str(port) + "/controller/nb/v2/hosttracker/default/hosts/active" #hosttracker stuff

	hosts = []
	h = httplib2.Http(".Cache")
	h.add_credentials(user,passw)
	resp,content = h.request(hosts_url,"GET")
	print "--------------"
	print content
	print "--------------"
	c = json.loads(content)
	for a in c["hostConfig"]:
		for b in range(len(nodes)):
			if nodes[b][0] == a["nodeId"]:
				hosts.append(a)
				#change the vlan to be from the list of vlans to IP addresses
				break
	return hosts

