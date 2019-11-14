class ISerializable:
    def GetBytes(self):
        pass

    def GetSize(self):
        pass


class Message(ISerializable):
    def __init__(self):
        self.Header = ISerializable()
        self.Body = ISerializable()

    def GetBytes(self):
        self.buffer = bytes(self.GetSize())

        self.header = self.Header.GetBytes()
        self.body = self.Body.GetBytes()

        return self.header + self.body

    def GetSize(self):
        return self.Header.GetSize() + self.Body.GetSize()
