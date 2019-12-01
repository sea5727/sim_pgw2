from pgw2memory import messageid_dict, calltype_dict
from PyInquirer import style_from_dict, Token
from commandline.cmdline_common import NumberValidator, IpValidator


style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})

Main_Question = [
    {
        'type': 'list',
        'name': 'Main_Question',
        'message': 'menu',
        'choices': [
                'Send_Message',
                'Show_Log ( file : ~~~.log )',
                'Mode',
                'Help',
                'Quit (Ctrl + C)',
        ],
    },
]

Send_Message_Question = [
    {
        'type': 'list',
        'name': 'Send_Message',
        'message': 'select message name',
        'choices': messageid_dict if messageid_dict.update({'Go_Back': -1}) is None else {},
        # 'when': lambda answers: answers['Main_Question'] == 'Send_Message', # asyncio 를 사용하려면 when이 없어야함.
    },
]


def GetModeQuestion(choices):
    Mode_Question = {
        'type': 'checkbox',
        'name': 'Mode_Question',
        'message': 'Set Mode',
        'choices': choices
    }
    return Mode_Question


Message_CallType_Question = [
    {
        'type': 'list',
        'name': 'call_type',
        'message': 'select a calltype',
        'choices': calltype_dict,
        # 'when': lambda answer: (
        #     answer['Send_Message'] != '_GW_STATUS' and
        #     answer['Send_Message'] != '_BUNCH_INFO'
        # )# asyncio 를 사용하려면 when이 없어야함.
    }
]


def test(value):
    return int(value)


def GetMessageMemberQuestion(messageClass):
    Message_Member_Question = [
        {
            'type': 'input',
            'name': name,
            'message': 'input {0}'.format(name),
            'validate': NumberValidator if name != 'media_ip' else IpValidator,
            # asyncio 를 사용하려면 filter가 없어야함.
            # 'filter': (lambda value: int(value)) if name != 'media_ip' else (lambda ip: struct.unpack('I', socket.inet_aton(ip))[0])
        } for name in messageClass.message_names if name != 'call_type'
    ]
    return Message_Member_Question


def GetConfirmQuestion(message):
    Confirm_Question = [
        {
            'type': 'confirm',
            'name': 'finallyOk',
            'message': message,
            'default': True
        }
    ]
    return Confirm_Question
