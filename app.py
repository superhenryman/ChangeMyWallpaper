from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/wallpaper")
def serve_wallpaper():
    if os.path.exists(UPLOAD_FOLDER) and os.path.join(UPLOAD_FOLDER, "wallpaper.png"):
        # ITS THERE
        return send_file(os.path.join(UPLOAD_FOLDER, "wallpaper.png"))
    else:
        print("Attempted sending file which doesn't exist")
        return "File not found", 404
    
@app.route("/submit", methods=["POST"])
def main():
    if os.path.exists("wallpaper.png"):
        try:
            os.remove("wallpaper.png")
        except Exception as e:
            print(f"Exception while deleting file {e}")
    file = request.files["file"]
    if file.filename == '':
        return "Empty filename", 69420
    if file and allowed_file(file):
        try:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
        except Exception as e:
            print(f"Error in main: {e}")
            return jsonify({
                "msg": f"Error occured in Main {e}",
                "code": "200"
            })
        finally:
            return jsonify({
            "msg": "Successfully changed wallpaper! Next time I boot up my PC, it'll be changed.",
            "code:": 200
        })
if __name__ == "__main__":
    app.run(debug=True)