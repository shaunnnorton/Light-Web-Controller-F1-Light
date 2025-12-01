from flask import Flask, render_template, request, jsonify
import time
import board
import neopixel
import random

app = Flask(__name__)
# The number of NeoPixels
num_pixels = 200
ORDER = neopixel.GRB


pixels = neopixel.NeoPixel(board.D18, 200, brightness=0.5, auto_write=False, pixel_order=neopixel.GRB)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/colors', methods=['POST'])
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


@app.route('/SinglePixelRandom', methods=['GET'])
def colors():
    color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    pixels[random.randint(1,30)] = color
    pixels.show()
    print(color)
    return jsonify({"message":"color recived"})



if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 80,debug=False)
