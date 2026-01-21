from flask import Flask, request, jsonify, render_template

import detection
from db_utils import save_results, load_result, get_stored_image_hashes, load_result_by_hash
import json
import os
import io
from PIL import Image

app = Flask(__name__)
HOST = "localhost"
PORT = 5000

LOCATIONS_FILE = "locations.json"

@app.route("/", methods=['GET'])
def testing_page():
    """Simple testing page"""
    return render_template("index.html", detect_path=f"http://{HOST}:{PORT}/detect-holds")

@app.route("/hello", methods=['GET'])
def hello():
    return "Hello, World!"



@app.route("/detect-holds", methods=['POST']) # TODO latitude longitude
def detect_holds():
    file = request.files.get("file", None)
    if file is None:
        return jsonify({"error": "No file provided"}), 400
    latitude = request.form.get("latitude", type=float)
    longitude = request.form.get("longitude", type=float)

    if latitude is None or longitude is None:
        latitude, longitude = 0, 0 #TODO FIX
        # return jsonify({"error": "No latitude and longitude provided"}), 400

    image = file.read()

    img = Image.open(io.BytesIO(image))
    image_width, image_height = img.size

    result = load_result(image)

    if result is None:
        print("No cached result, running detection...")
        result = detection.detect_holds(image)
        save_results(image, result)
    else:
        print("Loaded cached result.")

    coverage = calculate_coverage(result, image_width, image_height)
    result["coverage"] = coverage

    location_data = update_location_coverage(latitude, longitude, coverage)

    result["location"] = {
        "latitude" : latitude,
        "longitude": longitude,
        "average_coverage": location_data["average_coverage"],
        "count": location_data["count"]
        # "coverages": location_data["coverages"]
    }
    result_json = json.dumps(result)

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

# @app.route("/get-coverage")




def load_locations() -> dict:
    if os.path.exists(LOCATIONS_FILE):
        with open(LOCATIONS_FILE, 'r') as f:
            return json.load(f)
    return {"locations": []}

def save_locations(data):
    with open(LOCATIONS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def truncate_coords(lat:float, lon:float, decimals=2):
    return round(lat, decimals), round(lon, decimals)

def calculate_coverage(result, image_width, image_height):
    total_image_area = image_width * image_height
    total_holds_area = 0

    for hold in result.get("holds", []):
        if "size" in hold:
            total_holds_area += hold["size"][0] * hold["size"][1]
    # print(f"coverage: {total_holds_area}/{total_image_area}")

    return  total_holds_area/total_image_area

def update_location_coverage(lat, lon, coverage) ->dict:
    data = load_locations()
    trunc_lat, trunc_lon = truncate_coords(lat, lon)
    key = f"{trunc_lat},{trunc_lon}"
    if key in data:
        entry = data[key]
        count = entry["count"]
        avg = entry["average_coverage"]
        entry["average_coverage"] = (avg * count + coverage) / (count + 1)
        entry["count"] = count + 1
        entry["coverages"].append(coverage)
    else:
        data[key] = {
            "latitude": trunc_lat,
            "longitude": trunc_lon,
            "average_coverage": coverage,
            "count": 1,
            "coverages": [coverage]
        }

    save_locations(data)
    return data[key]

if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=PORT)


