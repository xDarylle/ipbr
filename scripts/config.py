import configparser
import os

class conf():
    def __init__(self):
        self.config_path = "../resources/config.ini"
        self.config = configparser.ConfigParser()
        if os.path.exists(self.config_path):
            self.load_conf()
        else:
            self.config.add_section("Settings")
            self.set_conf("","", "600", "900", [])
            self.load_conf()

    def load_conf(self):
        self.config.read(self.config_path)
        self.c = self.config["Settings"]
        self.output_path = self.c["output_path"]
        self.background = self.c["background"]
        self.width = self.c["width"]
        self.height = self.c["height"]
        self.bg_no = int(self.c["Number of BG"])
        self.background_array = []

        for i in range(int(self.bg_no)):
            self.background_array.append(self.c[str(i)])

    def get_conf(self):
        return self.output_path, self.background, self.width, self.height

    def set_conf(self, output_path, background, width, height, background_array):
        bg_no = len(background_array)
        self.config.set("Settings", "output_path", output_path)
        self.config.set("Settings", "background", background)
        self.config.set("Settings", "width", width)
        self.config.set("Settings", "height", height)
        self.config.set("Settings", "Number of BG", str(bg_no))

        for i in range(int(bg_no)):
            self.config.set("Settings", str(i), background_array[i])

        self.write()

    def get_output_path(self):
        return self.output_path

    def get_background(self):
        return self.background

    def get_array_backgrounds(self):
        return self.background_array

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_output_path(self, output_path):
        print(output_path)
        self.c["output_path"] = output_path

    def set_background(self, background):
        self.c["background"] = background

    def set_array_backgrounds(self, background_array):
        self.c["Number of BG"] = str(len(background_array))
        for i in range(len(background_array)):
             self.c[str(i)] = background_array[i]

    def set_width(self, width):
        print(width)
        self.c["width"] = width

    def set_height(self, height):
        self.c["height"] = height

    def write(self):
        self.f = open(self.config_path, "w+")
        self.config.write(self.f)
        self.f.close()
