from network import Network

node = Network("0.0.0.0")
node.start(5051)

#A peer started

node.join_network()
data=input()

while(True):
	node.broadcast(data)
	data=input()