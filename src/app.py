import os
from flask import Flask, render_template, request, redirect, url_for

# configure app to use src/static as static folder and src/templates for templates
app = Flask(__name__, template_folder="templates", static_folder="static")

UPLOAD_FOLDER = os.path.join(app.static_folder, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def upload_page():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "photo" not in request.files:
        return "No file part", 400
    file = request.files["photo"]
    if file.filename == "":
        return "No selected file", 400

    if file and allowed_file(file.filename):
        # keep original filename (for simplicity); production: sanitize/unique-ify
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(save_path)
        return redirect(url_for("gallery"))
    return "Invalid file type (allowed: png, jpg, jpeg, gif)", 400

@app.route("/gallery")
def gallery():
    allowed_ext = {"png", "jpg", "jpeg", "gif"}

    try:
        files = sorted(os.listdir(app.config["UPLOAD_FOLDER"]))
    except FileNotFoundError:
        files = []

    # Only keep real image files
    images = [
        f"/static/uploads/{f}"
        for f in files
        if "." in f and f.rsplit(".", 1)[1].lower() in allowed_ext
    ]

    return render_template("gallery.html", images=images)


if __name__ == "__main__":
    # for local development only; Docker will run the same command
    app.run(host="0.0.0.0", port=5000)

