# -*- coding: utf-8 -*-

import configparser


class Config(object):
    def __init__(self, path):
        self.config_path = path
        self.conf = configparser.ConfigParser()
        self.conf.optionxform = str
        self.conf.read(self.config_path)
 
    def get(self, field, key):
        return self.conf.get(field, key)

    def set(self, field, key, value):
        return self.conf.set(field, key, value)

    def save(self):
        with open(self.config_path, 'w') as f:
            self.conf.write(f, space_around_delimiters=False)


if __name__ == "__main__":
    config = Config("./config.ini")
    config.set("test", "HAHA", "D")
    config.save()
