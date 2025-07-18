from flask import Flask, request, send_file
import os
app = Flask(__name__)
IMAGE_PATH = "latest.jpg"

@app.route("/upload", methods=["POST"])
def upload():
    try:
        data = request.data
        if not data:
            return "No data received", 400

        with open(IMAGE_PATH, "wb") as f:
            f.write(data)

        print(f"[✓] Received frame: {len(data)} bytes")
        return "OK", 200
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        return "ERROR", 500

@app.route("/latest.jpg")
def get_latest():
    if not os.path.exists(IMAGE_PATH):
        return "Image not found", 404
    return send_file(IMAGE_PATH, mimetype="image/jpeg")

@app.route("/")
def index():
    return """
    <h1>ESP32-CAM Live Feed</h1>
    <img src="/latest.jpg" id="cam" width="320">
    <script>
      setInterval(() => {
        document.getElementById('cam').src = "/latest.jpg?t=" + new Date().getTime();
      }, 200);
    </script>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # use Railway’s dynamic port
    app.run(host="0.0.0.0", port=port)
