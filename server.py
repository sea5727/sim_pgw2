from twisted.internet import reactor, protocol
from messages import _PGW_MSG_HEAD
from define import _MESSAGE_ID


class MyProtocol(protocol.Protocol):
    def dataReceived(self, data):
        self.myScenario(data)
        # p 성공
        # p msg id로 메시지 할당
        # p 실패 ? 버림
        print("dataRecieved : ", data)
        self.transport.write(data)

    def myScenario(self, data):
        header = _PGW_MSG_HEAD(data)
        if(header.gw_msgid == _MESSAGE_ID.CALL_SETUP_REQ.value):
            print('hello call setup req')


class MyFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return MyProtocol()


def main():
    reactor.listenTCP(12345, MyFactory())
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
