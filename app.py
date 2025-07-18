from flask import Flask, request, send_file
import os

app = Flask(__name__)
IMAGE_PATH = "latest.jpg"

@app.route("/upload", methods=["POST"])
def upload():
    try:
        tmp_path = "tmp.jpg"
        with open(tmp_path, "wb") as f:
            f.write(request.data)
        os.replace(tmp_path, IMAGE_PATH)
        print(f"[✓] Frame saved: {len(request.data)} bytes")
        return "OK", 200
    except Exception as e:
        print(f"[ERROR] {e}")
        return "FAIL", 500

@app.route("/latest.jpg")
def get_latest():
    if not os.path.exists(IMAGE_PATH):
        return "Image not found", 404
    return send_file(IMAGE_PATH, mimetype="image/jpeg")

@app.route("/")
def index():
    return """
    <h1>ESP32-CAM Live Stream</h1>
    <img src="/latest.jpg" id="cam" width="320">
    <script>
      setInterval(() => {
        document.getElementById('cam').src = "/latest.jpg?t=" + new Date().getTime();
      }, 1000);
    </script>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # for Railway deployment
    app.run(host="0.0.0.0", port=port)
