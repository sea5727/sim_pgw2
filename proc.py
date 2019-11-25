from messages.body import (
    _GW_STATUS,
    _CALL_SETUP_REQ,
    _CALL_SETUP_RES,
    _MEDIA_ON_REQ,
    _MEDIA_ON_RES,
    _MEDIA_OFF_REQ,
    _MEDIA_OFF_RES,
    _MEDIA_ON_NOTI,
    _MEDIA_OFF_NOTI,
    _CALL_LEAVE_REQ,
    _CALL_LEAVE_RES,
    _CALL_END_NOTI,
    _BUNCH_INFO,
    _CALL_AUDIT_REQ,
    _CALL_AUDIT_RES)
from messages.message import _MESSAGE
from define.pgw_define import _CALL_TYPE
from call.CallManager import CallManager
import socket
import struct
import sys
from util import Util

__all__ = [
    'send_gw_status',
    'send_call_setup_req',
    'send_call_setup_res',
    'send_media_on_noti',
    'send_media_off_noti',
    'send_media_on_req',
    'send_media_on_res',
    'send_media_off_req',
    'send_media_off_res',
    'send_call_leave_req',
    'send_call_leave_res',
    'send_call_end_noti',
    'send_bunch_info']


test_ip = '192.168.0.166'


def send_gw_status(session, body=None, cmd=1, state=1):

    if body is None:
        body = _GW_STATUS()
        body.Init()
        body.cmd = cmd
        body.state = state

    msg = _MESSAGE(body)
    if Util.printf == 'on':
        msg.body.PrintDump()
        print('send(len:{0}) msg : {1}'.format(
            msg.GetSize(),
            msg.GetBytes()))

    session.transport.write(msg.GetBytes())
    

def send_call_setup_req(session, body=None, calltype=_CALL_TYPE._CT_PRIVATE, priority=1, reserve2=2, s_call_id=3, o_ssid=4, t_ssid=5, media_ip='127.0.0.1', media_port=7):
    if body is None:
        body = _CALL_SETUP_REQ()
        body.Init(calltype)
        body.priority = priority
        body.reserve2 = reserve2
        body.s_call_id = s_call_id
        body.o_ssid = o_ssid
        body.t_ssid = t_ssid
        body.media_ip = struct.unpack('=I', socket.inet_aton(media_ip))[0]
        body.media_port = media_port

    msg = _MESSAGE(body)
    if Util.printf == 'on':
        print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
        msg.body.PrintDump()
        print('send(len:{0}) msg : {1}'.format(
            msg.GetSize(),
            msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_call_setup_res(session, body=None, calltype=_CALL_TYPE._CT_PRIVATE, result=0, reserve2=1, s_call_id=2, r_call_id=3, media_ip='127.0.0.1', media_port=5):
    if body is None:
        body = _CALL_SETUP_RES()
        body.Init(calltype)
        body.result = result
        body.reserve2 = reserve2
        body.s_call_id = s_call_id
        body.r_call_id = r_call_id
        body.media_ip = struct.unpack('=I', socket.inet_aton(media_ip))[0]
        body.media_port = media_port

    msg = _MESSAGE(body)
    if Util.printf == 'on':
        print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
        msg.body.PrintDump()
        print('send(len:{0}) msg : {1}'.format(
            msg.GetSize(),
            msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_media_on_noti(session, body=None, calltype=_CALL_TYPE._CT_PRIVATE, reserve1=0, reserve2=0, r_call_id=3, o_ssid=4):
    if body is None:
        body = _MEDIA_ON_NOTI()
        body.Init(calltype)
        body.reserve1 = reserve1
        body.reserve2 = reserve2
        body.r_call_id = r_call_id
        body.o_ssid = o_ssid

    msg = _MESSAGE(body)
    if Util.printf == 'on':
        print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
        msg.body.PrintDump()
        print('send(len:{0}) msg : {1}'.format(
            msg.GetSize(),
            msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_media_off_noti(session, body=None, calltype=_CALL_TYPE._CT_PRIVATE, reason=0, reserve2=0, r_call_id=3):
    if body is None:
        body = _MEDIA_OFF_NOTI()
        body.Init(calltype)
        body.reason = reason
        body.reserve2 = reserve2
        body.r_call_id = r_call_id

    msg = _MESSAGE(body)
    if Util.printf == 'on':
        print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
        msg.body.PrintDump()
        print('send(len:{0}) msg : {1}'.format(
            msg.GetSize(),
            msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_media_on_req(session, body=None, calltype=_CALL_TYPE._CT_PRIVATE, o_priority=1, reserve2=0, r_call_id=3, o_ssid=4):
    if body is None:
        body = _MEDIA_ON_REQ()
        body.Init(calltype)
        body.o_priority = o_priority
        body.reserve2 = reserve2
        body.r_call_id = r_call_id
        body.o_ssid = o_ssid

    msg = _MESSAGE(body)
    if Util.printf == 'on':
        print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
        msg.body.PrintDump()
        print('send(len:{0}) msg : {1}'.format(
            msg.GetSize(),
            msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_media_on_res(session, body=None, calltype=_CALL_TYPE._CT_PRIVATE, result=0, reserve2=0, r_call_id=3, o_ssid=4):
    if body is None:
        body = _MEDIA_ON_RES()
        body.Init(calltype)
        body.result = result
        body.reserve2 = reserve2
        body.r_call_id = r_call_id
        body.o_ssid = o_ssid

    msg = _MESSAGE(body)
    if Util.printf == 'on':
        print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
        msg.body.PrintDump()
        print('send(len:{0}) msg : {1}'.format(
            msg.GetSize(),
            msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_media_off_req(session, body=None, calltype=_CALL_TYPE._CT_PRIVATE, reserve1=0, reserve2=0, r_call_id=3):
    if body is None:
        body = _MEDIA_OFF_REQ()
        body.Init(calltype)
        body.reserve1 = reserve1
        body.reserve2 = reserve2
        body.r_call_id = r_call_id

    msg = _MESSAGE(body)
    if Util.printf == 'on':
        print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
        msg.body.PrintDump()
        print('send(len:{0}) msg : {1}'.format(
            msg.GetSize(),
            msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_media_off_res(session, body=None, calltype=_CALL_TYPE._CT_PRIVATE, result=0, reserve2=0, r_call_id=3):
    if body is None:
        body = _MEDIA_OFF_RES()
        body.Init(calltype)
        body.result = result
        body.reserve2 = reserve2
        body.r_call_id = r_call_id

    msg = _MESSAGE(body)
    if Util.printf == 'on':
        print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
        msg.body.PrintDump()
        print('send(len:{0}) msg : {1}'.format(
            msg.GetSize(),
            msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_call_leave_req(session, body=None, calltype=_CALL_TYPE._CT_PRIVATE, reserve1=0, reserve2=0, r_call_id=3):
    if body is None:
        body = _CALL_LEAVE_REQ()
        body.Init(calltype)
        body.reserve1 = reserve1
        body.reserve2 = reserve2
        body.r_call_id = r_call_id

    msg = _MESSAGE(body)
    if Util.printf == 'on':
        print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
        msg.body.PrintDump()
        print('send(len:{0}) msg : {1}'.format(
            msg.GetSize(),
            msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_call_leave_res(session, body=None, calltype=_CALL_TYPE._CT_PRIVATE, result=0, reserve2=0, r_call_id=3):
    if body is None:
        body = _CALL_LEAVE_RES()
        body.Init(calltype)
        body.result = result
        body.reserve2 = reserve2
        body.r_call_id = r_call_id

    msg = _MESSAGE(body)
    if Util.printf == 'on':
        print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
        msg.body.PrintDump()
        print('send(len:{0}) msg : {1}'.format(
            msg.GetSize(),
            msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_call_end_noti(session, body=None, calltype=_CALL_TYPE._CT_PRIVATE, resason=0, reserve2=0, r_call_id=3):
    if body is None:
        body = _CALL_END_NOTI()
        body.Init(calltype)
        body.reason = resason
        body.reserve2 = reserve2
        body.r_call_id = r_call_id

    msg = _MESSAGE(body)
    if Util.printf == 'on':
        print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
        msg.body.PrintDump()
        print('send(len:{0}) msg : {1}'.format(
            msg.GetSize(),
            msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_bunch_info(session, body=None, cmd=1, reserve1=0, counter=3, bunch=[4, 5, 6]):
    if body is None:
        body = _BUNCH_INFO()
        body.Init()
        body.cmd = cmd
        body.reserve1 = reserve1
        body.counter = counter
        body.bunch = bunch

    msg = _MESSAGE(body)
    if Util.printf == 'on':
        print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
        msg.body.PrintDump()
        print('send(len:{0}) msg : {1}'.format(
            msg.GetSize(),
            msg.GetBytes()))
    session.transport.write(msg.GetBytes())


# def send_call_audit_req(session, body=None, calltype=_CALL_TYPE._CT_PRIVATE, r_call_id=3):
#     if body is None:
#         body = _CALL_AUDIT_REQ()
#         body.Init(calltype)
#         body.r_call_id = r_call_id

#     msg = _MESSAGE(body)
#     if Util.printf == 'on':
#         print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
#         msg.body.PrintDump()
#         print('send(len:{0}) msg : {1}'.format(
#             msg.GetSize(),
#             msg.GetBytes()))
#     session.transport.write(msg.GetBytes())


# def send_call_audit_res(session):
#     res = _CALL_AUDIT_RES()
#     res.Init(_CALL_TYPE._CT_PRIVATE)
#     res.r_call_id = 1
#     res.result = 2
#     res.expire_time = 3

#     msg = _MESSAGE(res)
#     if Util.printf == 'on':
#         print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
#         msg.body.PrintDump()
#         print('send(len:{0}) msg : {1}'.format(
#             msg.GetSize(),
#             msg.GetBytes()))
#     session.transport.write(msg.GetBytes())


def proc_test(session):
    send_call_setup_req(session)
    send_call_setup_res(session)
    send_media_on_noti(session)
    send_media_off_noti(session)
    send_media_on_req(session)
    send_media_on_res(session)
    send_media_off_req(session)
    send_media_off_res(session)
    send_call_leave_req(session)
    send_call_leave_res(session)
    send_call_end_noti(session)
    send_bunch_info(session)
