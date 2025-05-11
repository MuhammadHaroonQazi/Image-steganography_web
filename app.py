
from flask import Flask, render_template, request
import cv2
import numpy as np
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def data2binary(data):
    if type(data) == str:
        return ''.join([format(ord(i), '08b') for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        return [format(i, '08b') for i in data]
    return None

def hidedata(img, data):
    data += "$$"
    d_index = 0
    b_data = data2binary(data)
    len_data = len(b_data)

    for value in img:
        for pix in value:
            r = format(pix[0], '08b')
            g = format(pix[1], '08b')
            b = format(pix[2], '08b')

            if d_index < len_data:
                pix[0] = int(r[:-1] + b_data[d_index], 2)
                d_index += 1
            if d_index < len_data:
                pix[1] = int(g[:-1] + b_data[d_index], 2)
                d_index += 1
            if d_index < len_data:
                pix[2] = int(b[:-1] + b_data[d_index], 2)
                d_index += 1

            if d_index >= len_data:
                break
    return img


def find_data(img):
    bin_data = ""
    for value in img:
        for pix in value:
            r, g, b = data2binary(pix)
            bin_data += r[-1]
            bin_data += g[-1]
            bin_data += b[-1]
    all_bytes = [bin_data[i:i+8] for i in range(0, len(bin_data), 8)]
    readable_data = ""
    for byte in all_bytes:
        readable_data += chr(int(byte, 2))
        if readable_data[-2:] == "$$":
            break
    return readable_data[:-2]

@app.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':
        file = request.files['image']
        message = request.form['message']
        if file and message:
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(img_path)
            image = cv2.imread(img_path)
            encoded = hidedata(image, message)
            enc_img_name = "encoded_" + file.filename
            enc_path = os.path.join(app.config['UPLOAD_FOLDER'], enc_img_name)
            cv2.imwrite(enc_path, encoded)
            return render_template("encode.html", encoded_image=enc_img_name)
    return render_template("encode.html")

@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(img_path)
            image = cv2.imread(img_path)
            message = find_data(image)
            return render_template("decode.html", message=message)
    return render_template("decode.html")

if __name__ == '__main__':
    app.run(debug=True)
