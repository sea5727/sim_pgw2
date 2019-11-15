# import struct
# from define import _MESSAGE_ID, _CALL_TYPE


# class MESSAGE_BUFFER:   # common message class
#     buf = b""
#     labels = [
#     ]

#     def __init__(self, buf):
#         self.buf = buf
#         self.fmt = '!' + ''.join([label[1] for label in self.labels])
#         self.data = []
#         if buf and len(self.labels) > 0 and not len(buf) < self.__len__():
#             self.data += list(struct.unpack(self.fmt, buf[0: self.__len__()]))
#         else:
#             for idx, label in enumerate(self.labels):
#                 self.data.append(0)

#     def __getattr__(self, name):
#         for idx, label in enumerate(self.labels):
#             if label[0] == name:
#                 return self.data[idx]

#     def __setattr__(self, name, value):
#         if name in ['fmt', 'data', 'buf', 'labels']:
#             return object.__setattr__(self, name, value)
#         for idx, label in enumerate(self.labels):
#             if label[0] == name:
#                 self.data[idx] = value
#                 return self.data[idx]
#         raise ValueError

#     def __len__(self):
#         return struct.calcsize(self.fmt)

#     def Pack(self):
#         datas = [data for data in self.data]
#         return struct.pack(self.fmt, *datas)

#     def MakeHeader(self):
#         h = _PGW_MSG_HEAD()
#         h.gw_magic = h.magic
#         h.gw_msgid = self.msg_type.value
#         h.gw_length = self.__len__()
#         return h

#     def testprint(self):
#         print('self.buf : ', self.buf)
#         print('self.laels : ', self.labels)
#         print('self.fmt : ', self.fmt)
#         print('self.data : ', self.data)


# class _CALL_SETUP_REQ(MESSAGE_BUFFER):
#     msg_type = _MESSAGE_ID.CALL_SETUP_REQ
#     labels = []

#     def __init__(self, data=None, calltype=None):
#         if data and calltype:
#             return
#         if isinstance(type(calltype), type(_CALL_TYPE)):
#             self.labels = _CALL_TYPE.getLabels(calltype)
#         elif isinstance(type(data), bytes):
#             tmp_type = struct.unpack('=B', data[0:1])[0]
#             _CALL_TYPE.get_call_setup_req_labels(tmp_type)

#         super().__init__(data)
#         self.call_type = calltype.value


# class _PGW_MSG_HEAD(MESSAGE_BUFFER):   # b'\x47\x00\x??\x??'
#     magic = b'\x47'
#     msg_type = _MESSAGE_ID.PGW_MSG_HEAD
#     labels = [
#         ('gw_magic', 'B'),      # unsigned char
#         ('gw_msgid', 'B'),      # unsigned char
#         ('gw_length', 'H'),     # unsgiend short
#     ]


# def data_Received():
#     buf = b'\x47\x01\x00\x10abcdefasdasdfasdf12345'
#     print(buf)


# def call_setup_req():
#     call_setup_req = b'\x47\x01\x00\x10abcdefasdasdfasdf12345'
#     h = _PGW_MSG_HEAD(call_setup_req)
#     h.testprint()

#     if h.gw_msgid == _MESSAGE_ID.CALL_SETUP_REQ.value:
#         req = _CALL_SETUP_REQ(h.buf[h.__len__():])
#         print('msg : ', req.msg_type.name)


# def make_call_setup_req():
#     req = _CALL_SETUP_REQ(None, _CALL_TYPE.CT_PRIVATE)
#     print(req.call_type)
#     req.priority = 100
#     req.reserve2 = 0
#     req.call_id = 123123
#     req.o_ssid = 321312
#     req.t_ssid = 1231234
#     req.media_ip = 32
#     req.media_port = 5959
#     req.testprint()
#     buf = req.Pack()
#     print(buf)


# def main():
#     data_Received()


# # this only runs if the module was *not* imported
# if __name__ == '__main__':
#     main()
