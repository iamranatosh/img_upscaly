from flask import Flask, request, jsonify, send_file
import subprocess
import os
from PIL import Image

app = Flask(__name__)

@app.route('/upscale', methods=['POST'])
def upscale_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']
    image.save("input.jpg")

    # Run Real-ESRGAN inference
    subprocess.run([
        "python", "inference_realesrgan.py",
        "-i", "input.jpg",
        "-o", "output.jpg"
    ])

    return send_file("output.jpg", mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
