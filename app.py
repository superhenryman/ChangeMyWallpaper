from flask import Flask, request, send_file, jsonify, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/wallpaper")
def serve_wallpaper():
    wallpaper_path = os.path.join(UPLOAD_FOLDER, "wallpaper.png")
    if os.path.exists(wallpaper_path):
        return send_file(wallpaper_path)
    else:
        print("Attempted to send file which doesn't exist")
        return jsonify({"msg": "File not found", "code": 404}), 404

@app.route("/submit", methods=["POST"])
def main():
    wallpaper_path = os.path.join(UPLOAD_FOLDER, "wallpaper.png")

    file = request.files.get("file")
    if file is None or file.filename == '':
        return jsonify({"msg": "No file provided", "code": 400}), 400

    if not allowed_file(file.filename):
        return jsonify({"msg": "Invalid file type", "code": 400}), 400

    if os.path.exists(wallpaper_path):
        try:
            os.remove(wallpaper_path)
        except Exception as e:
            print(f"Error deleting file: {e}")
            return jsonify({"msg": f"Error deleting file: {e}", "code": 500}), 500
    try:
        file.save(wallpaper_path)
        return jsonify({"msg": "Successfully changed wallpaper! Next time I boot up my PC, it'll be changed.", "code": 200}), 200
    except Exception as e:
        print(f"Error saving file: {e}")
        return jsonify({"msg": f"Error saving file: {e}", "code": 500}), 500

if __name__ == "__main__":
    app.run(debug=True)
