#!/usr/bin/env python
from twisted.internet import stdio, reactor
from twisted.protocols import basic
from pgw_protocol import sessions
from util import Util
import proc


class CommandProtocol(basic.LineReceiver):
    delimiter = b'\n'   # unix terminal style newlines. remove this line
    # for use with Telnet

    def connectionMade(self):
        self.sendLine(b"cmd console. Type 'help' for help.")

    def lineReceived(self, line):
        # Ignore blank lines
        if not line:
            return
        line = line.decode("ascii")

        # Parse the command
        commandParts = line.split()
        command = commandParts[0].lower()
        args = commandParts[1:]

        # Dispatch the command to the appropriate method.  Note that all you
        # need to do to implement a new command is add another do_* method.
        try:
            method = getattr(self, 'do_' + command)
        except AttributeError as e:
            print(e)
            self.sendLine(b'Error: no such command.',)
        else:
            try:
                method(*args)
            except Exception as e:
                self.sendLine(b'Error: ' + str(e).encode("ascii"))

    def do_help(self, command=None):
        """help [command]: List commands, or show help on the given command"""
        if command is None:
            commands = [cmd[3:].encode("ascii")
                        for cmd in dir(self)
                        if cmd.startswith('do_')]
            self.sendLine(b"cmd list :  " + b" ".join(commands))
            self.print_main()
        else:
            doc = getattr(self, 'do_' + command).__doc__
            self.sendLine(doc.encode("ascii"))

    def do_server(self, *args):
        """client: Proc like server"""
        func = '_'.join(args)
        method = getattr(proc, func, lambda: 'Invalid proc')
        method(sessions['server'])

    def do_client(self, *args):
        """client: Proc like client"""
        func = '_'.join(args)
        method = getattr(proc, func, lambda: 'Invalid proc')
        method(sessions['client'])

    def send_msg(self, sock, msg):
        if sock is None:
            print('no connection sock:{0}, msg:{1}'.format(
                sock, msg
            ))
        else:
            print('sock:{0}, msg:{1}'.format(
                sock, msg
            ))

    def do_quit(self):
        """quit: Quit this session"""
        self.sendLine(b'Goodbye.')
        self.transport.loseConnection()

    def do_set(self, *args):
        getattr(self, args[0])(args[1])

    def hb(self, on_off):
        if on_off == 'on' or on_off == 'off':
            Util.hb = on_off

    def callid(self, number):
        Util.callid = int(number)

    def auto(self, on_off):
        if on_off == 'on' or on_off == 'off':
            Util.automode = on_off

    def print_main(self):
        print(" ")
        print("     help")
        print("     quit")
        print("     set hb [on/off] [{0}]".format(Util.hb))
        print("     set auto [on/off] [{0}]".format(Util.automode))
        print("     set callid [number] [{0}]".format(Util.callid))
        print("     client [function_name]")
        print("     server [function_name]")
        print(" ")

    # def do_check(self, url):
    #     """check <url>: Attempt to download the given web page"""
    #     url = url.encode("ascii")
    #     client.Agent(reactor).request(b'GET', url).addCallback(
    #         client.readBody).addCallback(
    #         self.__checkSuccess).addErrback(
    #         self.__checkFailure)

    # def __checkSuccess(self, pageData):
    #     msg = "Success: got {} bytes.".format(len(pageData))
    #     self.sendLine(msg.encode("ascii"))

    # def __checkFailure(self, failure):
    #     msg = "Failure: " + failure.getErrorMessage()
    #     self.sendLine(msg.encode("ascii"))

    def connectionLost(self, reason):
        # stop the reactor, only because this is meant to be run in Stdio.
        reactor.stop()


if __name__ == "__main__":
    stdio.StandardIO(CommandProtocol())
    reactor.run()
