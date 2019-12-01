import configparser


class Config:

    def __new__(cls, path=None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def Init(self, path, section):
        print('config read file')
        self.config = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))
        self.config.read(path)
        self.section = section

    def InitDefault(self):
        self.manual_log_path = 'pgw_default.log'
        self.manual_log_level = 'INFO'
        self.manual_log_stderr = 'on'
        self.manual_background = 'off'
        self.manual_connect_ip = '127.0.0.1'
        self.manual_connect_port = '54321'
        self.manual_listen_ip = '0.0.0.0'
        self.manual_listen_port = '12345'
        self.manual_listen_ctl = '5959'
        self.manual_reconnect_interval = 1
        self.manual_flag_automode = 'off'
        self.manual_flag_hb = 'off'
        self.manual_flag_rtp = 'off'

    def StringDump(self):
        dump = ''
        members = [attr for attr in dir(self) if (
            not callable(getattr(self, attr)) and
            not attr.startswith("__") and
            not attr in['config', 'instance']
            )]

        for member in members:
            dump += '{0} : {1} \n'.format(member, getattr(self, member))
        return dump

    @property
    def log_path(self):
        if hasattr(self, 'manual_log_path') and self.manual_log_path is not None:
            return self.manual_log_path
        return self.config[self.section]['log-path'] if self.config.has_option(self.section, 'log-path') else '.pgw2.log'

    @property
    def log_level(self):
        if hasattr(self, 'manual_log_level') and self.manual_log_level is not None:
            return self.manual_log_level
        return self.config[self.section]['log-level'] if self.config.has_option(self.section, 'log-level') else 'DEBUG'

    @property
    def log_stderr(self):
        if hasattr(self, 'manual_log_stderr') and self.manual_log_stderr is not None:
            return self.manual_log_stderr
        return self.config[self.section]['log-stderr'] if self.config.has_option(self.section, 'log-stderr') else 'off'

    @property
    def background(self):
        if hasattr(self, 'manual_background') and self.manual_background is not None:
            return self.manual_background
        return self.config[self.section]['background'] if self.config.has_option(self.section, 'background') else 'off'

    @property
    def connect_ip(self):
        if hasattr(self, 'manual_connect_ip') and self.manual_connect_ip is not None:
            return self.manual_connect_ip
        return self.config[self.section]['connect-ip'] if self.config.has_option(self.section, 'connect-ip') else '127.0.0.1'

    @property
    def connect_port(self):
        if hasattr(self, 'manual_connect_port') and self.manual_connect_port is not None:
            return int(self.manual_connect_port)
        return int(self.config[self.section]['connect-port']) if self.config.has_option(self.section, 'connect-port') else 12345

    @property
    def listen_ip(self):
        if hasattr(self, 'manual_listen_ip') and self.manual_listen_ip is not None:
            return self.manual_listen_ip
        return self.config[self.section]['listen-ip'] if self.config.has_option(self.section, 'listen-ip') else '0.0.0.0'

    @property
    def listen_port(self):
        if hasattr(self, 'manual_listen_port') and self.manual_listen_port is not None:
            return int(self.manual_listen_port)
        return int(self.config[self.section]['listen-port']) if self.config.has_option(self.section, 'listen-port') else 54321

    @property
    def listen_ctl(self):
        if hasattr(self, 'manual_listen_ctl') and self.manual_listen_ctl is not None:
            return int(self.manual_listen_ctl)
        return int(self.config[self.section]['listen-ctl']) if self.config.has_option(self.section, 'listen-ctl') else 5959

    @property
    def reconnect_interval(self):
        if hasattr(self, 'manual_reconnect_interval') and self.manual_reconnect_interval is not None:
            return float(self.manual_reconnect_interval)
        if self.config.has_option(self.section, 'reconnect-interval'):
            return float(self.config[self.section]['reconnect-interval'])
        else:
            return 1

    @property
    def flag_automode(self):
        if hasattr(self, 'manual_flag_automode') and self.manual_flag_automode is not None:
            return self.manual_flag_automode
        return self.config[self.section]['flag-automode'] if self.config.has_option(self.section, 'flag-automode') else 'off'

    @property
    def flag_hb(self):
        if hasattr(self, 'manual_flag_hb') and self.manual_flag_hb is not None:
            return self.manual_flag_hb
        return self.config[self.section]['flag-hb'] if self.config.has_option(self.section, 'flag-hb') else 'off'

    @property
    def flag_rtp(self):
        if hasattr(self, 'manual_flag_rtp') and self.manual_flag_rtp is not None:
            return self.manual_flag_rtp
        return self.config[self.section]['flag-rtp'] if self.config.has_option(self.section, 'flag-rtp') else 'off'


def main():
    pgw2Config = Config()
    print('1')
    testconf = Config()
    print('2')
    print(pgw2Config)
    print('3')
    print(testconf)
    print('4')
    testconf.Init('/home/jtas/workspace/pgw2/config.ini', 'DEV')
    print(testconf)
    test = Config()
    print(test)


if __name__ == '__main__':
    main()
