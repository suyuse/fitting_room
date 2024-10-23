from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from fal import process_images
import asyncio
from cloud import upload_image_to_cloudinary

os.environ["FAL_KEY"] = "51e1e97d-bde2-476e-b330-92f4ea45a257:c0a9de151ad33de6c57d37b319e9676c"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fit')
def fit():
    return render_template('fitting-room.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join('data/', filename)
        file.save(filepath)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        human = loop.run_until_complete(upload_image_to_cloudinary(filepath))
        result_image_url = process_images(human)
        print(result_image_url )
        return jsonify({'result_image': result_image_url})

    return jsonify({'error': 'No image provided'})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'photo' not in request.files:
        return 'No file part'
    file = request.files['photo']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('data/', filename))
        return 'File uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)
