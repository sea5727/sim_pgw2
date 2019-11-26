import configparser

class Config:

    test = None

    def __new__(cls, path=None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def Init(self, path):
        self.config = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))
        self.config.read(path)      
  
    # def __init__(self, path=None):
        
    #     self.config = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))
    #     print('__init__path:{0} config:{1}'.format(path, self.config))
    #     self.config.read(path)

    @property
    def open_ip(self):
        return self.config['SERVER']['ip'] if self.config.has_option('SERVER', 'ip') else '0.0.0.0'

    @property
    def open_port(self):
        return int(self.config['SERVER']['port']) if self.config.has_option('SERVER', 'port') else 54321

    @property
    def connect_ip(self):
        return self.config['CLIENT']['ip'] if self.config.has_option('CLIENT', 'ip') else '127.0.0.1'

    @property
    def connect_port(self):
        return int(self.config['CLIENT']['port']) if self.config.has_option('CLIENT', 'port') else 12345

    @property
    def automode(self):
        return self.config['PGW']['automode'] if self.config.has_option('PGW', 'automode') else 'off'

    @property
    def hb(self):
        return self.config['PGW']['hb'] if self.config.has_option('PGW', 'hb') else 'off'

    @property
    def rtp(self):
        return self.config['PGW']['rtp'] if self.config.has_option('PGW', 'rtp') else 'off'

    @property
    def log(self):
        return self.config['PGW']['log'] if self.config.has_option('PGW', 'log') else 'off'

    @property
    def std(self):
        return self.config['LOG']['std'] if self.config.has_option('LOG', 'std') else 'off'

    @property
    def log_path(self):
        return self.config['LOG']['path'] if self.config.has_option('LOG', 'path') else '.pgw2.log'

    @property
    def log_level(self):
        return self.config['LOG']['level'] if self.config.has_option('LOG', 'level') else 'DEBUG'
