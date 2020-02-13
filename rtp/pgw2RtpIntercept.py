class InterceptClient:
    def __init__(self, ip, port, filter_type, filter_value):
        self.ip = ip
        self.port = port
        self.filter_type = filter_type
        self.filter_value = filter_value

class InterceptManager:
    
    def __init__(self):
        self.list = []
    def makeClient(self, ip, port, filter_type, filter_value):
        return InterceptClient(ip, port, filter_type, filter_value)
    def addClient(self, interceptClient):
        self.list.append(interceptClient)

    def delClient(self, client):
        self.list.remove(client)

    def matchClient(self, call_setup_res_data):
        for idx in self.list:
            if hasattr(call_setup_res_data, idx.filter_type):
                value = getattr(call_setup_res_data, idx.filter_type, None)
                if type(value) == int and value == int(idx.filter_value): 
                    self.delClient(idx)
                    return idx                    
                if value == idx.filter_value:
                    self.delClient(idx)
                    return idx
                return None
