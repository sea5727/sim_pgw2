from pyfiglet import Figlet
from PyInquirer import style_from_dict, prompt, Token, Validator, ValidationError
selector_main = [
    {
        'type': 'list',
        'name': 'selector_main',
        'message': 'menu',
        'choices': [
            'Send Message', 
            'Show Log ( file : ~~~.log )',
            'Mode',
            'Help',
            'Quit (Ctrl + C)',
            ],
    },
]
send_message = [
    {
        'type': 'list',
        'name': 'send_message',
        'message': 'select a message',
        'choices': [
            'CALL_SETUP_REQ', 
            'CALL_SETUP_RES',
            'MEDIA_NOTI',
            ],
    },
]
style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})
f = Figlet()
import os
while 1:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f.renderText('PGW2 simulator'))
    answer = prompt(selector_main, style=style)
    print(answer)
    if answer['selector_main'] == 'Send Message':
        answer = prompt(send_message, style=style)
        print(answer)

