from flask import Flask, request, send_file
import os

app = Flask(__name__)
IMAGE_PATH = "latest.jpg"

@app.route("/upload", methods=["POST"])
def upload():
    with open(IMAGE_PATH, "wb") as f:
        f.write(request.data)
    return "OK", 200

@app.route("/latest.jpg")
def get_latest():
    return send_file(IMAGE_PATH, mimetype="image/jpeg")

@app.route("/")
def index():
    return """<h1>ESP32-CAM Stream</h1>
              <img src="/latest.jpg" id="cam" width="320">
              <script>
              setInterval(() => {
                const img = document.getElementById('cam');
                img.src = "/latest.jpg?t=" + new Date().getTime();
              }, 200);
              </script>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
