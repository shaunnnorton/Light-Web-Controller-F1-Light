import neopixel
import json



class Config(object):
    pixelcount = 0 
    frameshape = {}
    pixel_order = neopixel.GRB

    def __init__(self):
        with open("attributes.json") as attributes:
            jsondata = json.load(attributes)

        self.pixelcount = jsondata["pixels"]
        self.pixel_order = neopixel.GRB
        self.frameshape = jsondata["frameshape"]

    def get_updated_attributes(self):

        with open("attributes.json") as attributes:
            jsondata = json.load(attributes)

        self.pixelcount = jsondata["pixels"]
        self.pixel_order = neopixel.GRB
        self.frameshape = jsondata["frameshape"]

