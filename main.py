def arguments_and_config_set():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-file')
    parser.add_argument('-s', '--config-section')
    parser.add_argument('-L', '--log-level', help="DEBUG/INFO/FATAL")
    parser.add_argument('-E', '--log-stderr', action='store_true')
    parser.add_argument('-f', '--background', action='store_true')
    parser.add_argument("-i", "--connect-ip")
    parser.add_argument("-p", "--connect-port")
    parser.add_argument("-l", "--listen-port")
    
    args = parser.parse_args()

    from config.configure import pgw2Config as config

    if args.config_file:
        if args.config_section is None:
            raise Exception('input config-section')
        config.Init(args.config_file, args.config_section)
    else: 
        config.InitDefault()
        config.manual_log_level = args.log_level if args.log_level is not None else config.manual_log_level

        config.manual_log_stderr = args.log_stderr if args.log_stderr is not None else config.manual_log_stderr
        if config.manual_log_stderr == False:
            config.manual_log_stderr = 'off'

        config.manual_background = args.background if args.background is not None else config.manual_background
        if config.manual_background == False:
            config.manual_background = 'off'

        config.manual_connect_ip = args.connect_ip if args.connect_ip is not None else config.manual_connect_ip

        config.manual_connect_port = args.connect_port if args.connect_port is not None else config.manual_connect_port

        config.manual_listen_port = args.listen_port if args.listen_port is not None else config.manual_listen_port   

def input_cmd_run():
    import readline
    readline.parse_and_bind("tab: complete")

    class ARLCompleter:
        def __init__(self,logic):
            self.logic = logic

        def traverse(self,tokens,tree):
            if tree is None:
                return []
            elif len(tokens) == 0:
                return []
            if len(tokens) == 1:
                return [x+' ' for x in tree if x.startswith(tokens[0])]
            else:
                if tokens[0] in tree.keys():
                    return self.traverse(tokens[1:],tree[tokens[0]])
                else:
                    return []
            return []

        def complete(self,text,state):
            try:
                tokens = readline.get_line_buffer().split()
                if not tokens or readline.get_line_buffer()[-1] == ' ':
                    tokens.append('')
                results = self.traverse(tokens,self.logic) + [None]
                return results[state]
            except Exception as e:
                print(e)

    logic = {
        'build':
                {
                'barracks':None,
                'bar':None,
                'generator':None,
                'lab':None
                },
        'train':
                {
                'riflemen':None,
                'rpg':None,
                'mortar':None
                },
        'research':
                {
                'armor':None,
                'weapons':None,
                'food':None
                }
        }

    completer = ARLCompleter(logic)
    readline.set_completer(completer.complete)

    import time
    import sys
    import struct
    from twisted.internet import reactor
    from memory import sessions
    while 1:
        try:
            line = input('prompt> ')
            if sessions['command'] is None:
                continue
            sessions['command'].transport.write(line.encode())
        except KeyboardInterrupt as e: 
            print("Interrupt!")
            reactor.callFromThread(reactor.stop)
            break;


def main():

    arguments_and_config_set()

    from config.configure import pgw2Config as config
    from logger import pgw2logger as logger

    logger.info('######## START ##########')
    listen_port = config.listen_port
    connect_port = config.connect_port
    logger.info('open port : {0}, connect port : {1}'.format(listen_port, connect_port))

    
    from twisted.internet import protocol, reactor
    from server import Pgw2ServerFactory
    from client import Pgw2ClientFactory
    from cmdline import CmdFactory
    from twisted.internet import protocol
    from memory import sessions
    class CmdClient(protocol.Protocol):
        def connectionMade(self):
            self.transport.write(b"help")

    cmdClientSession = CmdClient()

    class CmdClientFactory(protocol.ClientFactory):
        def buildProtocol(self, addr):
            self.protocol = cmdClientSession
            sessions['command'] = self.protocol
            return self.protocol


    reactor.listenTCP(8888, CmdFactory())
    reactor.connectTCP("localhost", 8888, CmdClientFactory())
    reactor.listenTCP(listen_port, Pgw2ServerFactory())
    reactor.connectTCP(config.connect_ip, connect_port, Pgw2ClientFactory())

    from threading import Thread
    thread = Thread(target=reactor.run, args=(False,))
    thread.start()
    # reactor.run()
    
    input_cmd_run()
    

if __name__ == '__main__':
    main()
