import hashlib
import json
import os

RESULT_PATH = "results"

def save_results(image, results):
    """
    Stores the image results in a JSON file named by the image hash.
    """
    image_hash = hashlib.sha256(image).hexdigest()
    os.makedirs(RESULT_PATH, exist_ok=True)
    file_path = os.path.join(RESULT_PATH, f"{image_hash}.json")
    try:
        with open(file_path, "w") as f:
            json.dump(results, f)
    except Exception as e:
        print(f"Error saving results: {e}")
    return image_hash

def load_result(image):
    """
    Loads the image results from a JSON file named by the image hash.
    """
    image_hash = hashlib.sha256(image).hexdigest()
    file_path = os.path.join(RESULT_PATH, f"{image_hash}.json")
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r") as f:
            results = json.load(f)
        return results
    except Exception as e:
        print(f"Error loading results: {e}")
        return None

def get_stored_image_hashes():
    """
    Returns a list of all stored image hashes.
    """
    if not os.path.exists(RESULT_PATH):
        return []
    try:
        return [filename.split(".")[0] for filename in os.listdir(RESULT_PATH) if filename.endswith(".json")]
    except Exception as e:
        print(f"Error retrieving stored image hashes: {e}")
        return []

def load_result_by_hash(image_hash):
    """
    Loads the image results from a JSON file given the image hash.
    """
    file_path = os.path.join(RESULT_PATH, f"{image_hash}.json")
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r") as f:
            results = json.load(f)
        return results
    except Exception as e:
        print(f"Error loading results by hash: {e}")
        return None
