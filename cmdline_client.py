from twisted.internet import protocol
from pgw2memory import sessions

FLAG_EXIT = 'off'

class CmdClientProtocol(protocol.Protocol):
    
    def connectionMade(self):
        self.transport.write(b"help")

    def dataReceived(self, data):
        print(data.decode())
        if data.decode() == 'Goodbye.':
            FLAG_EXIT = 'on'


class CmdClientFactory(protocol.ReconnectingClientFactory):
    def buildProtocol(self, addr):
        self.protocol = CmdClientProtocol()
        sessions['command'] = self.protocol
        return self.protocol

    def clientConnectionFailed(self, connector, reason):
        self.maxDelay = 0.5
        super().clientConnectionFailed(connector, reason)

    def clientConnectionLost(self, connector, unused_reason):
        print('clientConnectionLost')
        self.maxDelay = 0.5
        super().clientConnectionLost(connector, unused_reason)


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

    messagename = {
        '_gw_status' : None,
        '_call_setup_req' : None,
        '_call_setup_res' : None,
        '_media_on_req' : None,
        '_media_on_res' : None,
        '_media_off_req' : None,
        '_media_off_res' : None,
        '_media_on_noti' : None,
        '_media_off_noti' : None,
        '_call_leave_req' : None,
        '_call_leave_res' : None,
        '_call_end_noti' : None,
        '_bunch_info' : None,
    }

    funcname = {'send' + message  : None for message in messagename}
    logic = {
        'help' : None,
        'quit': None,
        'show' : {
            'message' : messagename,
            'call' : None,
        },
        'set' : {
            'auto' : { 'on' : None, 'off' : None},
            'hb' : { 'on' : None, 'off' : None},
            'callid' : { 'on' : None, 'off' : None},
        },
        'client' : funcname,
        'server' : funcname
    }


    completer = ARLCompleter(logic)
    readline.set_completer(completer.complete)

    import time
    import sys
    import struct
    from twisted.internet import reactor
    from pgw2memory import sessions
    while FLAG_EXIT == 'off':
        try:
            line = input('prompt > ')
            if line == 'quit':
                break
            if sessions['command'] is None:
                continue
            sessions['command'].transport.write(line.encode())
            time.sleep(0.1)
        except KeyboardInterrupt as e: 
            break;

    reactor.callFromThread(reactor.stop)

def PyInquirerTest():
    import regex
    from pprint import pprint
    from PyInquirer import style_from_dict, prompt, Token
    from PyInquirer import Validator, ValidationError


    class PhoneNumberValidator(Validator):
        def validate(self, document):
            ok = regex.match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text)
            if not ok:
                raise ValidationError(
                    message='Please enter a valid phone number',
                    cursor_position=len(document.text))  # Move cursor to end

    class NumberValidator(Validator):
        def validate(self, document):
            try:
                int(document.text)
            except ValueError:
                raise ValidationError(
                    message='Please enter a number',
                    cursor_position=len(document.text))  # Move cursor to end



    questions = [
        {
            'type': 'confirm',
            'name': 'toBeDelivered',
            'message': 'Is this for delivery?',
            'default': False
        },
        {
            'type': 'input',
            'name': 'phone',
            'message': 'What\'s your phone number?',
            'validate': PhoneNumberValidator
        },
        {
            'type': 'list',
            'name': 'size',
            'message': 'What size do you need?',
            'choices': ['Large', 'Medium', 'Small'],
            'filter': lambda val: val.lower()
        },
        {
            'type': 'input',
            'name': 'quantity',
            'message': 'How many do you need?',
            'validate': NumberValidator,
            'filter': lambda val: int(val)
        },
        {
            'type': 'expand',
            'name': 'toppings',
            'message': 'What about the toppings?',
            'choices': [
                {
                    'key': 'p',
                    'name': 'Pepperoni and cheese',
                    'value': 'PepperoniCheese'
                },
                {
                    'key': 'a',
                    'name': 'All dressed',
                    'value': 'alldressed'
                },
                {
                    'key': 'w',
                    'name': 'Hawaiian',
                    'value': 'hawaiian'
                }
            ]
        },
        {
            'type': 'rawlist',
            'name': 'beverage',
            'message': 'You also get a free 2L beverage',
            'choices': ['Pepsi', '7up', 'Coke']
        },
        {
            'type': 'input',
            'name': 'comments',
            'message': 'Any comments on your purchase experience?',
            'default': 'Nope, all good!'
        },
        {
            'type': 'list',
            'name': 'prize',
            'message': 'For leaving a comment, you get a freebie',
            'choices': ['cake', 'fries'],
            'when': lambda answers: answers['comments'] != 'Nope, all good!'
        }
    ]

    from define.pgw_define import _MESSAGE_ID
    
    myquestions = [
        {
            'type': 'input',
            'name': 'quantity',
            'message': 'How many do you need?',
            'validate': NumberValidator,
            'filter': lambda val: int(val)
        },
        {
            'type': 'list',
            'name': 'message-name',
            'message': 'select a message',
            'choices': {msg_id.name : msg_id.value for msg_id in _MESSAGE_ID },
            'validate': NumberValidator
            # 'filter': lambda val: val.lower()
        },
        {
            'type': 'list',
            'name': 'calltype',
            'message': 'select a calltype',
            'choices': ['CT_PRIVATE', 'CT_GROUP', 'CT_EMER', 'CT_UDG', 'CT_ALERT', 'CT_RPC'],
            # 'when' : lambda answers: answers['message-name'] != '_GW_STATUS' and answers['message-name'] != '_BUNCH_INFO'
        },
    ]

    style = style_from_dict({
        Token.QuestionMark: '#E91E63 bold',
        Token.Selected: '#673AB7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#2196f3 bold',
        Token.Question: '',
    })

    from messages import body
    test = [getattr(body, msg_id.name) for msg_id in _MESSAGE_ID]

    # answers = prompt(questions, style=style)
    # pprint(answers)

    msg_names = prompt(myquestions, style=style)
    print(msg_names)
    pprint(msg_names)

    



def cmdtest():
    import sys
    port = 5959
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    from twisted.internet import reactor
    reactor.connectTCP("localhost", port, CmdClientFactory())

    from threading import Thread
    thread = Thread(target=reactor.run, args=(False,))
    thread.start()

    input_cmd_run()


if __name__ == '__main__':
    PyInquirerTest()

