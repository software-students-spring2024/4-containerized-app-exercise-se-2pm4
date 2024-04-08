from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load environment variables
mongo_uri = os.environ.get('MONGO_URI')
flask_port = os.environ.get('FLASK_RUN_PORT', 5000)

client = MongoClient(mongo_uri)
db = client['image_emotion_db']
images_collection = db['images']

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        image_file = request.files['image']
        if image_file:
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(file_path)
            
            # Insert into DB
            object_id = images_collection.insert_one({
                'image_ref': file_path,
                'processed': False,
                'emotion': 'none'
            }).inserted_id
            
            return jsonify({'message': 'Image uploaded successfully', 'object_id': str(object_id)})
    
    return render_template('home.html')

@app.route('/gallery')
def gallery():
    images = images_collection.find()
    return render_template('gallery.html', images=images)

@app.route('/status/<object_id>')
def check_status(object_id):
    image_data = images_collection.find_one({'_id': ObjectId(object_id)})
    if image_data:
        return jsonify({
            'processed': image_data['processed'],
            'emotion': image_data['emotion']
        })
    return jsonify({'error': 'Image not found'}), 404

if __name__ == '__main__':
    app.run(port=flask_port)