from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

class MultiClientEcho(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.append(self)

    def dataReceived(self, data):
        for client in self.factory.clients:
            client.transport.write(data)
            print (client)
            print ("data in server %s" %data)


    def connectionLost(self, reason):
        self.factory.clients.remove(self)


class MultiClientEchoFactory(Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
            return MultiClientEcho(self)


reactor.listenTCP(8000, MultiClientEchoFactory())
reactor.run()
