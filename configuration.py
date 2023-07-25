import os

class Configuration:
    def __init__(self):
        self.configfile = 'mbg.conf'
        self.config = { 'screenres': '640x480',
                        'defaultserver': '',
                        'servermode': 'False',
                        'sound': 'True' }
        
        if (os.path.exists(self.configfile)):
            f = open(self.configfile)
            for line in f.readlines():
                (key, value) = line.strip().split("=", 1)
                self.config[key] = value

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value
        f=open(self.configfile, "w")
        for (key, value) in self.config.items():
            f.write("%s=%s\n" % (key, value))

config = Configuration()