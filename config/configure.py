import configparser


class Config:

    def __init__(self):
        self.config = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))
        self.config.read('./config.ini')

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
    def printf(self):
        return self.config['PGW']['printf'] if self.config.has_option('PGW', 'printf') else 'off'

pgwConfig = Config()
