from twisted.internet import protocol, reactor
from ... import cmdline

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        print("data received : ", data)
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

reactor.listenTCP(8888, EchoFactory())
reactor.run()