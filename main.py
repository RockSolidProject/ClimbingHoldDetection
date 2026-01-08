from flask import Flask, request, jsonify, render_template
from db_utils import save_results, load_result, get_stored_image_hashes
import detect

app = Flask(__name__)

@app.route("/", methods=['GET'])
def testing_page():
    """Simple testing page"""
    return render_template("index.html")

@app.route("/hello", methods=['GET'])
def hello():
    return "Hello, World!"

@app.route("/detect-holds", methods=['POST'])
def detect_holds():
    file = request.files.get("file", None)
    if file is None:
        return jsonify({"error": "No file provided"}), 400
    image = file.read()
    test_images(file.filename, image)

    result = load_result(image)
    if result is None:
        print("No cached result, running detection...")
        result = detect.detect_holds(image)
        save_results(image, result)
    else:
        print("Loaded cached result.")

    return jsonify(result)

def test_images(filename, image):
    """SAVES THE IMAGE TO TEST IF SUCESUFULLY UPLOADED"""
    import os
    save_path = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(image)

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000)
