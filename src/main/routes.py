from flask import Flask, render_template, request, jsonify, Blueprint, flash,redirect, url_for
import os
import time
import board
import neopixel
import random
from src.utils import prepUploads as pu
from .. import config


appconfig = config.Config()

main = Blueprint("main", __name__)

print(appconfig.pixelcount)
print(appconfig.pixel_order)

# The number of NeoPixels
num_pixels = appconfig.pixelcount
ORDER = appconfig.pixel_order

UPLOAD_FOLDER = "/src/static/schedules"


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


def allowed_file_upload(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ("xlsx", "xls")

@main.route('/UploadNewFile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file_upload(file.filename):
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))

            uploadparse = pu.parseUploadedExcel(os.path.join(UPLOAD_FOLDER, file.filename))


            flash(uploadparse)
            return redirect(url_for('index'))
    return '''
    <!doctype html>
    <title>Upload new Schedule File</title>
    <h1>Upload new Schedule File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''