#!/usr/bin/env python
from twisted.internet import stdio, reactor
from twisted.internet.protocol import Protocol
from pgw2memory import sessions
from messages import body
from call.CallManager import CallManager
from protocol import proc
import socket
import struct
from pgw2memory import pgw2Config as config
from logger.pyLogger import LogManager as logger

class CommandProtocol(Protocol):
    delimiter = b'\n'   # unix terminal style newlines. remove this line
    # for use with Telnet
    def __init__(self):
        super().__init__()
        self.messages = {msgname : getattr(body, msgname)().Init() for msgname in body.__all__}


    def connectionMade(self):
        self.sendLine(b"cmd console. Type 'help' for help.")

    def dataReceived(self, data):
        print('data Received')

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
        """server: Proc like server"""
        func = '_'.join(args)
        method = getattr(proc, func, lambda: 'Invalid proc')
        if method == proc.send_all_message:
            proc.send_all_message(session=sessions['server'])
            return
        classname = '_' + '_'.join(args[1:]).upper()        
        method(session=sessions['server'], body=self.messages[classname])

    def do_client(self, *args):
        """client: Proc like client"""
        func = '_'.join(args)
        method = getattr(proc, func, lambda: 'Invalid proc')
        if method == proc.send_all_message:
            proc.send_all_message(session=sessions['client'])
            return
        classname = '_' + '_'.join(args[1:]).upper()
        method(session=sessions['client'], body=self.messages[classname])

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
        """set: set args"""
        getattr(self, 'set_' + args[0])(*args[1:])

    def do_show(self, *args):
        """show: print infomation"""
        if args[0] == 'call':
            if args[1] == 'status':
                CallManager.printCallStatus()
                return
        if args[0] == 'message':
            if args[1] == 'all':
                for msg_key in self.messages:
                    self.messages[msg_key].PrintDump()
                return
            msgname = '_'.join(args[1:]).upper()
            if msgname not in self.messages:
                if '_' + msgname in self.messages:
                    msgname = '_' + msgname
            self.messages[msgname].PrintDump()


    def do_reset(self, *args):
        """show: print infomation"""
        print('todo')

    def set_message(self, *args):
        set_value = []
        cmd_list = list(args)
        
        for cmd in args:
            if '=' in cmd:
                set_value.append(cmd)
                cmd_list.remove(cmd)

        msgname = '_'.join(cmd_list).upper()
        if msgname not in self.messages:
            if '_' + msgname in self.messages:
                msgname = '_' + msgname

        for setter in set_value:
            set = setter.split('=')
            cur_value = getattr(self.messages[msgname], set[0])
            if set[0] == 's_call_id' and type(self.messages[msgname]) is body._CALL_SETUP_REQ: 
                print('use set callid instead set message')
                return
            if set[0] == 'call_type':
                print('if you set call_type, this message is clear')
                self.messages[msgname] = getattr(body, msgname)().Init(int(set[1]))
                self.messages[msgname].PrintDump()
                return
            if set[0] == 'media_ip':
                setattr(self.messages[msgname], set[0], struct.unpack('=I', socket.inet_aton(set[1]))[0] )
                self.messages[msgname].PrintDump()
                return
            # print('cur value:{0}, cur type:{1}, new value:{2}, new type:{3}'.format(cur_value, type(cur_value), set[1], type(set[1])))
            setattr(self.messages[msgname], set[0], int(set[1]))

        self.messages[msgname].PrintDump()

    def set_hb(self, *args):
        on_off = args[0]
        if on_off != 'on' and on_off != 'off':
            return
        if on_off == 'on':
            sessions['client'].hb.start(10, now=True)
        elif on_off == 'off':
            sessions['client'].hb.stop()

        config.set_flag_hb = on_off

    def set_callid(self, *args):
        number = args[0]
        CallManager.CallId = int(number)

    def set_auto(self, *args):
        on_off = args[0]
        if on_off == 'on' or on_off == 'off':
            print('todo set auto')

    def set_loglevel(self, *args):
        level = args[0]
        level = level.upper()
        if level not in ('DEBUG' , 'INFO', 'WARNING', 'FATAL', 'CRITICAL'):
            return

        config.manual_log_level = level
        logger.set_loglevel(level)

    def print_main(self):
        print(" ")
        print("     help")
        print("     quit")
        print("     show message [msgname]")
        print("     show call [status]  ")
        print("     reset flag          ")
        print("     set auto [on/off] [{0}]".format(config.flag_automode))
        print("     set hb [on/off] [{0}]".format(config.flag_hb))
        # print("     set rtp [on/off] [{0}]".format(config.flag_rtp))
        print("     set callid [number] [{0}]".format(CallManager.CallId))
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


