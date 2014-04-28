import tornado.ioloop
import tornado.web
import config_parser
import topology_commands
import get_graph

global nodes
global connections
global daylight_ip
global daylight_port

#daylight_ip = '172.24.240.19'
daylight_ip = '172.16.6.12'
daylight_port = '8080'

nodes = []
connections = []

user = "admin"
passw = "admin"

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		html = """<!DOCTYPE html>
		<html>
		<head>
			<title>Wow</title>
		</head>
		<body>
			<form action="/openslice" id="open_slice" method="post">
					<input type="submit" value="Submit">
			</form>
			Starting Node: <select name="node_1" form="open_slice">"""
		count = 0
		for a in nodes:
			html += '<option value="'+str(count)+'">' + str(a[1]) + '</option>\n'
			count += 1
		html += "</select><br>\n"
		html += 'Ending Node: <select name="node_2" form="open_slice">' 
		count = 0
		for a in nodes:
			html += '<option value="'+str(count)+'">' + str(a[1]) + '</option>\n'
			count += 1
		html += """		</select><br>
					</body>
				</html>"""


		self.write(html)
        
class OpenSliceHandler(tornado.web.RequestHandler):
	def post(self):
		global nodes
		global connections
		node_1 = self.get_argument('node_1','Not Selected')
		node_2 = self.get_argument('node_2','Not Selected')
		print node_1
		print node_2
		x = topology_commands.build_slice(nodes[int(node_1)],nodes[int(node_2)],nodes,connections)
		html =  "node_1: "+str(nodes[int(node_1)][1])+"<br>"
		html += "node_2: "+str(nodes[int(node_2)][1])+"<br>"
		html += str([nodes[a][1] for a in x])
		self.write(html)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/openslice", OpenSliceHandler),
])

if __name__ == "__main__":

	config = False
	print "wow"
	if config:
		nodes,connections = config_parser.parse_config("config.txt")
	else:
		nodes,connections = get_graph.get_graph(daylight_ip,daylight_port,user,passw)
	hosts = get_graph.get_hosts(daylight_ip,daylight_port,user,passw,nodes)
	print "Nodes: ",nodes
	print "Connections: ",connections
	print "Hosts: ",hosts

	topology_commands.build_base_rules(daylight_ip,
	daylight_port,
	user,
	passw,
	nodes,
	connections,
	hosts)



	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()