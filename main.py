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

        config.manual_background = args.background if args.background is not None else config.manual_background



def main():

    arguments_and_config_set()

    from config.configure import pgw2Config as config
    from logger import pgw2logger as logger

    
    listen_port = config.listen_port
    connect_ip = config.connect_ip
    connect_port = config.connect_port
    ctl_port = config.listen_ctl

    logger.info('############### START ##############')
    logger.info('connect ip : {0} , connect port : {1}'.format(connect_ip, connect_port))
    logger.info('listen port : {0} , ctl port : {1}'.format(listen_port, ctl_port))
    
    from twisted.internet import reactor
    from server import Pgw2ServerFactory
    from client import Pgw2ClientFactory
    from cmdline import CmdServerFactory
    from cmdline_client import CmdClientFactory

    reactor.listenTCP(listen_port, Pgw2ServerFactory())
    reactor.connectTCP(config.connect_ip, connect_port, Pgw2ClientFactory())

    reactor.listenTCP(ctl_port, CmdServerFactory())

    if config.background == 'off':
        reactor.connectTCP("localhost", config.listen_ctl, CmdClientFactory())

        from threading import Thread
        thread = Thread(target=reactor.run, args=(False,)).start()
        from cmdline_client import input_cmd_run
        
        input_cmd_run()
    else:
        reactor.run()
    

if __name__ == '__main__':
    main()
