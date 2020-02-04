import json
from twisted.internet import reactor, protocol
from messages import body
from pgw2memory import calltype_dict, pgw2Config as config
from pgw2memory import sessions
from protocol import proc
from logger.pyLogger import pgw2logger as logger


class PgwCommandLineServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return PgwCommandLineServer()


class PgwCommandLineServer(protocol.Protocol):

    def connectionMade(self):
        print('cmd line protocol connectio made!!')

    def dataReceived(self, data):
        if not data:
            return
        str_data = data.decode("utf-8")
        logger.debug(str_data)
        obj_data = json.loads(str_data)

        if 'request' not in obj_data:
            return
        request = 'Do_' + obj_data['request'].lower()
        if hasattr(self, request) is False:
            return
        getattr(self, request)(session=self, data=obj_data)

    def Do_get(self, session, data):
        if data is None:
            return
        Res = {}
        if data['subject'] == 'config_log_path':
            Res['log_path'] = config.log_path
        str_data = json.dumps(Res).replace(' ', '')
        session.transport.write(str_data.encode())

    def Do_get_help(self, session, data):
        Help = {
            'help': 'Show infomation',
            'log_path': config.log_path,
            'log_level': config.log_level,
            'listen_ip': config.listen_ip,
            'listen_port': config.listen_port,
            'connect_ip': config.connect_ip,
            'connect_port': config.connect_port,
            'listen_ctl': config.listen_ctl,
            'flag_automode': config.flag_automode,
            'flag_hb': config.flag_hb,
            'flag_rtp': config.flag_rtp,
        }
        str_data = json.dumps(Help).replace(' ', '')
        session.transport.write(str_data.encode())

    def Do_get_mode_choices(self, session, data=None):
        Mode = {'Mode_Choices': [
            {
                'name': 'autoResponse',
                'checked': True if config.flag_automode == 'on' else False
            },
            {
                'name': 'autoHB',
                'checked': True if config.flag_hb == 'on' else False
            },
            {
                'name': 'autoRTP',
                'checked': True if config.flag_rtp == 'on' else False
            },
        ]}
        str_data = json.dumps(Mode).replace(' ', '')
        session.transport.write(str_data.encode())

    def Do_set_mode_choices(self, session=None, data=None):
        if data is None:
            return
        for flag in data['Mode_Choices']:
            if flag['name'] == 'autoResponse':
                config.manual_flag_automode = 'on' if flag['checked'] is True else 'off'
            elif flag['name'] == 'autoHB':
                config.manual_flag_hb = 'on' if flag['checked'] is True else 'off'
            elif flag['name'] == 'autoRTP':
                config.manual_flag_rtp = 'on' if flag['checked'] is True else 'off'

    def Do_send_message(self, session=None, data=None):
        print('Do_send_message')
        if data is None:
            return

        message_name = data['message_name']
        messageClass = None
        if message_name in ['_GW_STATUS', '_BUNCH_INFO']:
            # _GW_STATUS, _BUCH_INFO 같은경우 CallType이 필요없음.
            messageClass = getattr(body, message_name)()
            messageClass.Init()
        else:
            messageClass = getattr(body, message_name)()
            messageClass.Init(calltype_dict[data['datas']['call_type']])

        for data_name, data_value in data['datas'].items():
            if data_name == 'call_type':    # 위에서 세팅
                continue
            setattr(messageClass, data_name, data_value)
        getattr(proc, 'send' + message_name.lower())(sessions['client'], messageClass)


def main():
    reactor.listenTCP(5959, PgwCommandLineServerFactory())
    reactor.run()


if __name__ == '__main__':
    main()
