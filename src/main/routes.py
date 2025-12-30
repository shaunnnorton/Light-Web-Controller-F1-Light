from flask import Flask, render_template, request, jsonify, Blueprint
import time
import board
import neopixel
import random
from .. import config


appconfig = config.Config()

main = Blueprint("main", __name__)

print(appconfig.pixelcount)
print(appconfig.pixel_order)

# The number of NeoPixels
num_pixels = appconfig.pixelcount
ORDER = appconfig.pixel_order




pixels = neopixel.NeoPixel(board.D18, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER)

@main.route('/')
def index():
    rows = sorted(appconfig.frameshape.keys())
    columns = sorted(appconfig.frameshape[rows[0]].keys())
    return render_template('index.html', rows=rows, columns=columns)


@main.route('/colors', methods=['POST'])
def colors():
    data = request.json
    color = data.get('colordata')
    print(color)
    color = color.lstrip('#')
    color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    pixels.fill(color)
    pixels.show()
    print(color)
    return jsonify({"message":"color recived"})


@main.route('/SinglePixelRandom', methods=['GET'])
def singlePixelRandom():
    color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    pixels[random.randint(1,30)] = color
    pixels.show()
    print(color)
    return jsonify({"message":"color recived"})


@main.route('/SetBoxColor', methods=['GET'])
def SetBoxColor():
    appconfig.get_updated_attributes()

    row = request.args.get("row")
    col = request.args.get("column")
    color = request.args.get("color")
    print(color)
    color = color.lstrip('#')
    color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

    for pixel in appconfig.frameshape[row][col]["PIXELS"]:
        pixels[pixel-1] = color

    pixels.show()
    print(color)

    return jsonify({"message":"color recived"})


@main.route('/Automatic', methods=['GET'])
def AutomaticUpdate():
    appconfig.get_updated_attributes()

    row = request.args.get("row")
    col = request.args.get("column")
    
    background_color = (255,255,255)
    color = (255,0,0)
    pixels.fill(background_color)

    print(color)
    for pixel in appconfig.frameshape[row][col]["PIXELS"]:
        pixels[pixel-1] = color
    pixels.show()
    print(color)

    return jsonify({"message":"color recived"})


