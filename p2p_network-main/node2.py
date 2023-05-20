from network import Network

node = Network("localhost")
node.start(5052)

#A peer started

node.join_network()
data = {
'id': 'fbc019f3a87787f904b54875f62e2193445f0e0f4e82f6978d77dbe29d7a9894',
'title': '#BROADCAST',
'message': 'Hello world',
'time': 1617555967.1199386
}

while(True):
	node.broadcast(data)
	data=input()