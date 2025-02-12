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

    # Run Real-ESRGAN inference and capture errors
    try:
        result = subprocess.run([
            "python", "inference_realesrgan.py",
            "-i", "input.jpg",
            "-o", "output.jpg"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 500

        return send_file("output.jpg", mimetype='image/jpeg')

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
