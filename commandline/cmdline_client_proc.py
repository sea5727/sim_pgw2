from PyInquirer import prompt
from pyfiglet import Figlet
from pgw2memory import calltype_dict
from commandline.cmdline_client_format import Main_Question, Send_Message_Question
from commandline.cmdline_client_format import Message_CallType_Question, GetModeQuestion
from commandline.cmdline_client_format import style
from commandline.cmdline_client_format import GetMessageMemberQuestion
from commandline.cmdline_client_format import GetConfirmQuestion
from messages import body
import os
import asyncio
import socket
import struct
import json
import time
import subprocess
import select


class PgwCommandLineClient:
    async def InitSession(self, server_ip, server_port):
        print('InitSession start..?')
        self.loop = asyncio.get_event_loop()
        self.reader, self.writer = await asyncio.open_connection(server_ip, server_port)

    def Run(self):
        f = Figlet()

        while 1:
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f.renderText('PGW2 simulator'))
                answer = prompt(Main_Question, style=style)

                if len(answer) == 0:
                    break

                question_selected = answer['Main_Question'].split(' ', maxsplit=1)[0]
                print('your select : ', question_selected)

                final_message = getattr(self, 'Do_' + question_selected)()

                if question_selected == 'Quit':
                    break
                elif question_selected == 'Show_Log':
                    continue
                elif question_selected == 'Help':
                    continue
                elif question_selected == 'Send_Message':
                    if final_message is None:
                        return
                    final_message['request'] = 'Send_Message'
                    write_data = json.dumps(final_message).replace(' ', '')
                    self.WriteCoroutine(write_data.encode())
                elif question_selected == 'Mode':
                    if final_message is None:
                        return
                    final_message = {
                        'request': 'Set_Mode_Choices',
                        'Mode_Choices': final_message
                    }
                    write_data = json.dumps(final_message).replace(' ', '')
                    self.WriteCoroutine(write_data.encode())
            except Exception:
                print('except')
            # except Exception as e:
            #     print('except', e)
            #     break

    def Do_Show_Log(self):
        request = {
            'request': 'Get',
            'subject': 'config_log_path'
        }
        message = json.dumps(request).replace(' ', '')
        self.WriteCoroutine(message.encode())
        read_data = self.ReadCoroutine(1)
        config_path = json.loads(read_data.decode())

        f = subprocess.Popen(
            ['tail', '-18f', config_path['log_path']],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        p = select.poll()
        p.register(f.stdout)

        while 1:
            try:
                if p.poll(0.1):
                    print(f.stdout.readline().decode(), end='')
                time.sleep(0.01)
            except KeyboardInterrupt:
                break

    def Do_Quit(self):
        print('Quit')

    def WriteCoroutine(self, byte):
        self.writer.write(byte)
        self.loop.run_until_complete(self.writer.drain())

    def ReadCoroutine(self, sec):
        result = self.loop.run_until_complete(asyncio.wait_for(self.reader.read(8096), sec))
        return result

    def Do_Help(self):
        try:
            request = {
                'request': 'Get_Help'
            }
            message = json.dumps(request).replace(' ', '')

            self.WriteCoroutine(message.encode())
            read_data = self.ReadCoroutine(1)

            Help = json.loads(read_data.decode())
            for key, value in Help.items():
                print('{0} : {1}'.format(key, value))
            input("Press Enter to continue...")
        except KeyboardInterrupt:
            return

    def Do_Mode(self):
        print('Do_Mode')
        request = {
            'request': 'Get_Mode_Choices'
        }
        message = json.dumps(request).replace(' ', '')

        self.WriteCoroutine(message.encode())
        read_data = self.ReadCoroutine(1)

        Mode_Choices = json.loads(read_data.decode())['Mode_Choices']
        answer = prompt(GetModeQuestion(Mode_Choices), style=style)
        selected_modes = answer['Mode_Question']


        for idx, value in enumerate(Mode_Choices):
            Mode_Choices[idx]['checked'] = False
            for selected in selected_modes:
                if value['name'] == selected:
                    Mode_Choices[idx]['checked'] = True
        return Mode_Choices

    def Do_Send_Message(self):
        print('Do_Send_Message')
        answer = prompt(Send_Message_Question, style=style)
        message_name = answer['Send_Message']
        if message_name == 'Go_Back':
            return

        final_message = {}
        final_message['message_name'] = message_name

        messageClass = None
        final_message['datas'] = {}
        if message_name in ['_GW_STATUS', '_BUNCH_INFO']:
            # _GW_STATUS, _BUCH_INFO 같은경우 CallType이 필요없음.
            messageClass = getattr(body, message_name)()
            messageClass.Init()
        else:
            answer = prompt(Message_CallType_Question, style=style)
            call_type = answer['call_type']
            final_message['datas']['call_type'] = call_type
            messageClass = getattr(body, message_name)()
            messageClass.Init(calltype_dict[call_type])

        message_member = GetMessageMemberQuestion(messageClass)
        message_member.extend(GetConfirmQuestion('Is this for Send??'))

        answer = prompt(message_member, style=style)
        for key, value in answer.items():
            if key == 'finallyOk':
                if value is False:
                    return None
                break
            if key == 'media_ip':
                final_message['datas'][key] = struct.unpack('I', socket.inet_aton(value))[0]
            else:
                final_message['datas'][key] = int(value)

        return final_message


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    cmdlineClient = PgwCommandLineClient()
    loop.run_until_complete(cmdlineClient.InitSession('127.0.0.1', 5959))
    try:
        cmdlineClient.Run()
    except Exception:
        print('Main Except..')
