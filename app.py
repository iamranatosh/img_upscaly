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

    try:
        # Run Real-ESRGAN inference and capture stdout and stderr
        result = subprocess.run([
            "python", "inference_realesrgan.py",
            "-i", "input.jpg",
            "-o", "output.jpg"
        ], capture_output=True, text=True, timeout=600)  # timeout set to 600 sec for example

        # Log the subprocess output (you can also write this to a file)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 500

        # Check if output file was created
        if not os.path.exists("output.jpg"):
            return jsonify({"error": "Output file not created"}), 500

        return send_file("output.jpg", mimetype='image/jpeg')

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Processing timed out"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
