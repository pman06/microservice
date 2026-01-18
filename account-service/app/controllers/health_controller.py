from flask  import jsonify

def health_controller():
    return jsonify({"status": "healthy"}), 200