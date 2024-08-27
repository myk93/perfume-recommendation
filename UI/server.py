from flask import Flask, jsonify, request, render_template, send_from_directory
import json
import random
import os

app = Flask(__name__, static_folder='static')


# Use os.path.join for platform-independent paths
data_file_path = os.path.join(app.static_folder, 'New_Data_set.json')

# Load the JSON data
try:
    with open(data_file_path, 'r') as f:
        perfumes = json.load(f)
except FileNotFoundError:
    perfumes = []
    print(f"Error: {data_file_path} not found.", file=sys.stderr)

@app.route('/')
@app.route('/index')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/recommend', methods=['POST'])
def recommend_perfume():
    user_collection = request.json.get('collection', []) # those are the perfumes in collection
    if user_collection:
        # add here the logic for deciding which perfume to bring back to app currently random from collection or from data set
        random_perfume = random.choice(user_collection)
        return jsonify([random_perfume])
    if perfumes:
        random_perfume = random.choice(perfumes)
        return jsonify([random_perfume])
    else:
        return jsonify([]), 404

@app.route('/collection')
def collection():
    return app.send_static_file('collection.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
