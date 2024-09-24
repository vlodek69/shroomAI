import os

import dill
import redis
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

from utils.predict import predict

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config["REDIS_URL"] = os.getenv("REDIS_URL")
redis_client = redis.StrictRedis.from_url(app.config["REDIS_URL"])


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/upload")
def upload():
    return render_template("upload.html")


@app.route("/prediction", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        try:
            prediction = predict(img=file)
            dilled_shroom = redis_client.get(prediction["index"])
            shroom = dill.loads(dilled_shroom)

            predicted_shroom_dict = {
                **shroom.serialize(),
                "probability": prediction["probability"],
            }

            return jsonify(predicted_shroom_dict), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run()
