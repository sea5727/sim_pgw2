from twisted.internet import protocol
from pgw2memory import sessions
import readline
import struct
import ipaddress
import socket
from PyInquirer import style_from_dict, prompt, Token
from PyInquirer import Validator, ValidationError
from pgw2memory import messageid_dict, calltype_dict


class CmdManager:
    FLAG_EXIT = 'off'


class CmdClientProtocol(protocol.Protocol):

    def connectionMade(self):
        self.transport.write(b"help")

    def dataReceived(self, data):
        print(data.decode())
        if data.decode() == 'Goodbye.':
            CmdManager.FLAG_EXIT = 'on'


class CmdClientFactory(protocol.ReconnectingClientFactory):
    def buildProtocol(self, addr):
        self.protocol = CmdClientProtocol()
        sessions['command'] = self.protocol
        return self.protocol

    def clientConnectionFailed(self, connector, reason):
        self.maxDelay = 0.5
        super().clientConnectionFailed(connector, reason)

    def clientConnectionLost(self, connector, unused_reason):
        self.maxDelay = 0.5
        super().clientConnectionLost(connector, unused_reason)


class ARLCompleter:
    def __init__(self, logic):
        self.logic = logic

    def traverse(self, tokens, tree):
        if tree is None:
            return []
        elif len(tokens) == 0:
            return []
        if len(tokens) == 1:
            return [x + ' ' for x in tree if x.startswith(tokens[0])]
        else:
            if tokens[0] in tree.keys():
                return self.traverse(tokens[1:], tree[tokens[0]])
            else:
                return []
        return []

    def complete(self, text, state):
        try:
            tokens = readline.get_line_buffer().split()
            if not tokens or readline.get_line_buffer()[-1] == ' ':
                tokens.append('')
            results = self.traverse(tokens, self.logic) + [None]
            return results[state]
        except Exception as e:
            print(e)


def input_cmd_run():
    readline.parse_and_bind("tab: complete")
    messagename = {
        '_gw_status': None,
        '_call_setup_req': None,
        '_call_setup_res': None,
        '_media_on_req': None,
        '_media_on_res': None,
        '_media_off_req': None,
        '_media_off_res': None,
        '_media_on_noti': None,
        '_media_off_noti': None,
        '_call_leave_req': None,
        '_call_leave_res': None,
        '_call_end_noti': None,
        '_bunch_info': None,
        'all': None
    }

    funcname = {'send' + message: None for message in messagename}

    logic = {
        'help': None,
        'quit': None,
        'show': {
            'message': messagename,
            'call': None,
        },
        'set': {
            'message': None,
            'auto': {'on': None, 'off': None},
            'hb': {'on': None, 'off': None},
            'callid': {'on': None, 'off': None},
        },
        'client': funcname,
        'server': funcname
    }

    completer = ARLCompleter(logic)
    readline.set_completer(completer.complete)

    import time
    from twisted.internet import reactor
    from pgw2memory import sessions
    while CmdManager.FLAG_EXIT == 'off':
        try:
            time.sleep(0.1)
            line = input('prompt > ')
            if line.find('quit') == 0:
                break
            if line.find('set message') == 0:
                set_message_json = MessageSetPrompt()
                sessions['command'].transport.write(
                    b'set message ' + set_message_json.encode())
                continue
            if sessions['command'] is None:
                continue
            sessions['command'].transport.write(line.encode())

        except KeyboardInterrupt:
            break

    reactor.callFromThread(reactor.stop)


def MessageSetPrompt():

    class IpValidator(Validator):
        def validate(self, document):
            try:
                ipaddress.ip_address(document.text)
            except ValueError:
                raise ValidationError(
                    message='Please enter a ip',
                    cursor_position=len(document.text))  # Move cursor to end

    class NumberValidator(Validator):
        def validate(self, document):
            try:
                int(document.text)
            except ValueError:
                raise ValidationError(
                    message='Please enter a number',
                    cursor_position=len(document.text))  # Move cursor to end

    myquestions = [
        {
            'type': 'list',
            'name': 'message_name',
            'message': 'select a message',
            'choices': messageid_dict,
        },
        {
            'type': 'list',
            'name': 'call_type',
            'message': 'select a calltype',
            'choices': calltype_dict,
            'when': lambda mssage_name: (
                mssage_name['message_name'] != '_GW_STATUS' and
                mssage_name['message_name'] != '_BUNCH_INFO'
                )
        },
    ]

    style = style_from_dict({
        Token.QuestionMark: '#E91E63 bold',
        Token.Selected: '#673AB7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#2196f3 bold',
        Token.Question: '',
    })

    # answers = prompt(questions, style=style)
    # pprint(answers)
    from messages import body

    selected_message = prompt(myquestions, style=style)
    messageClass = None
    if (selected_message['message_name'] != '_GW_STATUS' and
            selected_message['message_name'] != '_BUNCH_INFO'):
        messageClass = getattr(body, selected_message['message_name'])()
        messageClass.Init(calltype_dict[selected_message['call_type']])
    else:
        messageClass = getattr(body, selected_message['message_name'])()
        messageClass.Init()

    def int_filter(value):
        return int(value)

    def ip_filter(ip):
        return struct.unpack('I', socket.inet_aton(ip))[0]

    data_questions = [
        {
            'type': 'input',
            'name': name,
            'message': 'input {0}'.format(name),
            'validate': NumberValidator if name != 'media_ip' else IpValidator,
            'filter': int_filter if name != 'media_ip' else ip_filter
        } for name in messageClass.message_names if name != 'call_type'
    ]

    selected_data = prompt(data_questions, style=style)
    selected_message.update(selected_data)
    import json
    set_message_json = json.dumps(selected_message)
    return set_message_json.replace(' ', '')


def cmdtest():
    port = 5959

    from twisted.internet import reactor
    reactor.connectTCP("localhost", port, CmdClientFactory())

    from threading import Thread
    thread = Thread(target=reactor.run, args=(False,))
    thread.start()

    input_cmd_run()


if __name__ == '__main__':
    cmdtest()
    # MessageSetPrompt()
