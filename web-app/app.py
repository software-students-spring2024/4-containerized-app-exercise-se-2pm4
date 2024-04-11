"""OS module used for creating filepaths and getting envs"""

import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# load environment variables
# mongo_uri = os.environ.get("MONGO_URI")
flask_port = os.environ.get("FLASK_RUN_PORT")
MONGO_HOST = os.environ.get("DB_HOST", "mongodb_server")

# Load environment variables for MongoDB connection
MONGO_PORT = os.environ.get("MONGO_PORT", 27017)
MONGO_DB = os.environ.get("MONGO_DB", "image_emotion_db")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
mongo_uri = f"mongodb://{DB_USER}:{DB_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
client = MongoClient(mongo_uri)
# db = client["image_emotion_db"]
db = client.get_database(MONGO_DB)
images_collection = db["images"]


@app.route("/", methods=["GET", "POST"])
def home():
    """function for loading the home page"""
    if request.method == "POST":
        image_file = request.files["image"]
        if image_file:
            # create a unique filename using current timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = secure_filename(f"{timestamp}_{image_file.filename}")
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(file_path)

            # insert into DB
            object_id = images_collection.insert_one(
                {"image_ref": file_path, "processed": False, "emotion": "loading..."}
            ).inserted_id
            print(object_id)
            return jsonify(
                {"message": "Image uploaded successfully", "object_id": str(object_id)}
            )

    return render_template("home.html")


@app.route("/gallery")
def gallery():
    """function for loading gallery"""
    images = images_collection.find()
    return render_template("gallery.html", images=images)


@app.route("/status/<object_id>")
def check_status(object_id):
    """function for checking status"""
    image_data = images_collection.find_one({"_id": ObjectId(object_id)})
    if image_data:
        return jsonify(
            {"processed": image_data["processed"], "emotion": image_data["emotion"]}
        )
    return jsonify({"error": "Image not found"}), 404


if __name__ == "__main__":
    app.run(debug = True, port=flask_port)
