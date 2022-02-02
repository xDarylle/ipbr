import configparser
import os

class conf():
    def __init__(self):
        self.config_path = "../resources/config.ini"
        self.config = configparser.ConfigParser()
        if os.path.exists(self.config_path):
            self.load_conf()
        else:
            self.f = open(self.config_path, "w+")
            self.config.add_section("Settings")
            self.set_conf("","", "", "")
            self.load_conf()

    def load_conf(self):
        self.config.read(self.config_path)
        self.c = self.config["Settings"]
        self.output_path = self.c["output_path"]
        self.background = self.c["background"]
        self.width = self.c["width"]
        self.height = self.c["height"]

    def get_conf(self):
        return self.output_path, self.background, self.width, self.height

    def set_conf(self, output_path, background, width, height):
        self.config.set("Settings", "output_path", output_path)
        self.config.set("Settings", "background", background)
        self.config.set("Settings", "width", width)
        self.config.set("Settings", "height", height)
        self.config.write(self.f)


    def get_output_path(self):
        return self.output_path

    def get_background(self):
        return self.background

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_output_path(self, output_path):
        print(output_path)
        self.c["output_path"] = output_path

    def set_background(self, background):
        self.c["background"] = background

    def set_width(self, width):
        print(width)
        self.c["width"] = width

    def set_height(self, height):
        self.c["height"] = height

    def write(self):
        self.f = open(self.config_path, "w+")
        self.config.write(self.f)
