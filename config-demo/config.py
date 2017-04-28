# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser


class CustomConfig(ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    def write(self, fp):
        """Write an .ini-format representation of the configuration state."""
        if self._defaults:
            fp.write("[%s]\n" % "DEFAULT")
            for (key, value) in self._defaults.items():
                fp.write("%s = %s\n" % (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                if key == "__name__":
                    continue
                if (value is not None) or (self._optcre == self.OPTCRE):
                    key = "=".join((key, str(value).replace('\n', '\n\t')))
                fp.write("%s\n" % (key))
            fp.write("\n")


class Config(object):
    def __init__(self, path):
        self.config_path = path
        self.conf = CustomConfig()
        self.conf.optionxform = str
        self.conf.read(self.config_path)
 
    def get(self, field, key):
        return self.conf.get(field, key)

    def set(self, field, key, value):
        return self.conf.set(field, key, value)

    def save(self):
        with open(self.config_path, 'w') as f:
            self.conf.write(f)


if __name__ == "__main__":
    config = Config("./config.ini")
    config.set("test", "HAHA", "D")
    config.save()
