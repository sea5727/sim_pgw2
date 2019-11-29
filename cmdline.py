#!/usr/bin/env python
from twisted.internet import stdio, reactor
from twisted.internet import protocol
from pgw2memory import sessions
from messages import body
from call.CallManager import CallManager
import proc
from config.configure import pgw2Config as config
from logger import LogManager
from logger import pgw2logger as logger


class CmdServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return CommandProtocol()


class CommandProtocol(protocol.Protocol):
    delimiter = b'\n'   # unix terminal style newlines. remove this line

    def __init__(self):
        super().__init__()
        self.messages = {
            msgname: getattr(body, msgname)().Init() for msgname in body.__all__
            }

    def connectionMade(self):
        logger.debug('cmd line protocol connection made!!')
        # self.transport.write("Hello, world!")
        # self.sendLine(b"cmd console. Type 'help' for help.")

    def dataReceived(self, line):
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
            for arg in e.args:
                self.transport.write(arg.encode())
            self.transport.write(b'Error: no such command.',)
            # self.sendLine(b'Error: no such command.',)
        else:
            try:
                method(*args)
            except Exception as e:
                # self.sendLine(b'Error: ' + str(e).encode("ascii"))
                self.transport.write(b'Error: ' + str(e).encode("ascii"))

    def do_help(self, command=None):
        """help [command]: List commands, or show help on the given command"""
        if command is None:
            commands = [cmd[3:].encode("ascii")
                        for cmd in dir(self)
                        if cmd.startswith('do_')]
            # self.sendLine(b"cmd list :  " + b" ".join(commands))
            self.transport.write(b"cmd list :  " + b" ".join(commands) + b'\n')
            self.print_main()
        else:
            doc = getattr(self, 'do_' + command).__doc__
            self.transport.write(doc.encode("ascii"))
            # self.sendLine(doc.encode("ascii"))

    def do_server(self, *args):
        """server: Proc like server"""
        func = '_'.join(args)
        method = getattr(proc, func, lambda: 'Invalid proc')
        if method == proc.send_all_message:
            proc.send_all_message(session=sessions['server'])
            return
        if len(args) == 1:
            classname = args[0].replace('send', '').upper()
            method(session=sessions['server'], body=self.messages[classname])
        else:
            classname = '_' + '_'.join(args[1:]).upper()
            method(session=sessions['server'], body=self.messages[classname])

    def do_client(self, *args):
        """client: Proc like client"""
        func = '_'.join(args)
        method = getattr(proc, func, lambda: 'Invalid proc')
        if method == proc.send_all_message:
            proc.send_all_message(session=sessions['client'])
            return
        if len(args) == 1:
            classname = args[0].replace('send', '').upper()
            method(session=sessions['server'], body=self.messages[classname])
        else:
            classname = '_' + '_'.join(args[1:]).upper()
            method(session=sessions['server'], body=self.messages[classname])

    def do_quit(self):
        """quit: Quit this session"""
        # self.sendLine(b'Goodbye.')
        self.transport.write(b'Goodbye.')
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
                    self.transport.write(self.messages[msg_key].StringDump().encode() + b'\n')
                return
            msgname = '_'.join(args[1:]).upper()
            if msgname not in self.messages:
                if '_' + msgname in self.messages:
                    msgname = '_' + msgname
            self.transport.write(self.messages[msgname].StringDump().encode())

    def do_reset(self, *args):
        """show: print infomation"""
        self.transport.write(b'todo')

    def set_message(self, *args):
        import json
        from pgw2memory import calltype_dict
        set_messages = args[0]
        message_dict = json.loads(set_messages)
        message_name = message_dict['message_name']
        message_dict.pop('message_name')

        for data_name, data_value in message_dict.items():
            if data_name == 'call_type':
                setattr(self.messages[message_name], data_name, calltype_dict[data_value])
            else:
                setattr(self.messages[message_name], data_name, data_value)

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
            self.transport.write(b'todo set auto')

    def set_loglevel(self, *args):
        level = args[0]
        level = level.upper()
        if level not in ('DEBUG', 'INFO', 'WARNING', 'FATAL', 'CRITICAL'):
            return

        config.manual_log_level = level
        LogManager.set_loglevel(level)

    def print_main(self):
        newline = '\n'
        msg = ''
        msg += '     help' + newline
        msg += '     quit' + newline
        msg += '     show message [msgname]' + newline
        msg += '     show call [status]' + newline
        msg += '     reset flag' + newline
        msg += '     set auto [on/off] [{0}]'.format(config.flag_automode) + newline
        msg += '     set hb [on/off] [{0}]'.format(config.flag_hb) + newline
        msg += '     set callid [number] [{0}]'.format(CallManager.CallId) + newline
        msg += '     client [function_name]' + newline
        msg += '     server [function_name]' + newline
        msg += ' ' + newline
        self.transport.write(msg.encode())

    def connectionLost(self, reason):
        print('connectionLost')
        # reactor.stop()


if __name__ == "__main__":
    stdio.StandardIO(CommandProtocol())
    reactor.run()
