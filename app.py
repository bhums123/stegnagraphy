from flask import Flask, render_template, request, send_file
from PIL import Image # type: ignore
import numpy as np
import io

app = Flask(__name__,) # type: ignore

def encode_image(image_path, secret_text):
    image = Image.open(image_path)
    encoded_image = image.copy()
    data = np.array(encoded_image)
    binary_secret_text = ''.join(format(ord(i), '08b') for i in secret_text)
    data_flat = data.flatten()
    
    for i in range(len(binary_secret_text)):
        data_flat[i] = (data_flat[i] & ~1) | int(binary_secret_text[i])
    
    encoded_image = Image.fromarray(data_flat.reshape(data.shape))
    return encoded_image

def decode_image(image_path):
    image = Image.open(image_path)
    data = np.array(image)
    binary_secret_text = ''
    
    for pixel in data.flatten():
        binary_secret_text += str(pixel & 1)
    
    # Convert binary to string
    secret_text = ''.join(chr(int(binary_secret_text[i:i+8], 2)) for i in range(0, len(binary_secret_text), 8))
    return secret_text.rstrip('\x00')

@app.route('/')
def index():
    return render_template('index.html') # type: ignore

@app.route('/encrypt', methods=['POST'])
def encrypt():
    file = request.files['image'] # type: ignore
    secret_text = request.form['text'] # type: ignore
    image = encode_image(file, secret_text)
    
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return send_file(img_byte_arr, mimetype='image/png') # type: ignore

@app.route('/decrypt', methods=['POST'])
def decrypt():
    file = request.files['image'] # type: ignore
    if file:
        secret_text = decode_image(file)  # Ensure this function works correctly
        return secret_text  # Return the actual decrypted text
    return "No file uploaded", 400

if __name__ == '__main__':
    app.run(debug=True)
    