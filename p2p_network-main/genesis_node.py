from network import Network

peer = Network("0.0.0.0")
peer.start(5050)


data=input()

while(True):
	peer.broadcast(data)
	data=input()
