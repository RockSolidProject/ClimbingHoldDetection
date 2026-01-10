from flask import Flask, request, jsonify, render_template

import detection
from db_utils import save_results, load_result, get_stored_image_hashes, load_result_by_hash

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
    import base64
    file = request.files.get("file", None)
    if file is None:
        return jsonify({"error": "No file provided"}), 400
    image = file.read()
    test_images(file.filename, image)

    result = load_result(image)
    if result is None:
        print("No cached result, running detection...")
        result = detection.detect_holds(image)
        save_results(image, result)
    else:
        print("Loaded cached result.")

    annotated_img_b64 = None
    if result.get("annotated_image"):
        annotated_img_b64 = base64.b64encode(result["annotated_image"]).decode('utf-8')
        result["annotated_image"] = annotated_img_b64
    return jsonify(result)

@app.route("/stored-hashes", methods=['GET'])
def stored_hashes():
    hashes = get_stored_image_hashes()
    return jsonify({"hashes": hashes})

@app.route("/result-by-hash/<image_hash>", methods=['GET'])
def result_by_hash(image_hash):
    result = load_result_by_hash(image_hash)
    if result is None:
        return jsonify({"error": "No result found for this hash"}), 404
    return jsonify(result)



def test_images(filename, image):
    """SAVES THE IMAGE TO TEST IF SUCESUFULLY UPLOADED"""
    import os
    save_path = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(image)

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
