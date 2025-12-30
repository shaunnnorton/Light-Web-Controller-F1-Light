import neopixel
import json



class Config(object):
    pixelcount = 0 
    frameshape = {}
    pixel_order = neopixel.GRB
    currentScheduleFile = ""
    automatic_refresh = True

    def __init__(self):
        with open("attributes.json") as attributes:
            jsondata = json.load(attributes)

        self.pixelcount = jsondata["pixels"]
        self.pixel_order = neopixel.GRB
        self.frameshape = jsondata["frameshape"]
        self.currentScheduleFile = jsondata["currentScheduleFile"]
        self.automatic_refresh = True

    def get_updated_attributes(self):

        with open("attributes.json") as attributes:
            jsondata = json.load(attributes)

        self.pixelcount = jsondata["pixels"]
        self.pixel_order = neopixel.GRB
        self.frameshape = jsondata["frameshape"]
        self.currentScheduleFile = jsondata["currentScheduleFile"]

