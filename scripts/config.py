import os
import configparser

class conf():
    def __init__(self):
        config_path = "../resources/config.ini"
        self.config = configparser.ConfigParser()
        if os.path.exists(config_path):
            self.c = self.config.read(config_path)
            self.settings = self.c["Settings"]
            self.output_path = self.settings["output_path"]
            self.background = self.settings["background"]
            self.width = self.settings["width"]
            self.height = self.settings["height"]
        else:
            self.f = open(config_path, "w+")
            self.config.add_section("Settings")
            self.set_conf("","", "", "")


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
        self.settings["output_path"] = output_path

    def set_background(self, background):
        self.settings["background"] = background

    def set_width(self, width):
        self.settings["width"] = width

    def set_height(self, height):
        self.settings["height"] = height

