from twisted.internet import reactor, protocol

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(b"help")

    def dataReceived(self, data):
        print("Server said:", data)
        # self.transport.loseConnection()

class EchoFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.", reason.getErrorMessage())

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")

reactor.connectTCP("localhost", 8888, EchoFactory())
reactor.run()
