from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import os

SECRET_URI = os.getenv('SECRET_URI')

app = Flask(__name__, template_folder="static/templates")
client = MongoClient(SECRET_URI)
db = client['mikeslab']

licenses_collection = db['licenses']
files_collection = db['files']


#
# Verifies the license
#
def verify_license(license_key):
    license_result = licenses_collection.find_one({"licenseKey": license_key})
    return license_result is not None


#
# GET mapping for '/'
#
@app.route('/')
def index():
    return render_template('index.html')

#
# GET mapping '/access'
#
@app.route('/access/<path:path>', methods=['GET'])
def access_folder(path):
    license_key = request.headers.get('License-Key')

    if verify_license(license_key):
        file = files_collection.find_one({"path": path})

        if file is not None:
            return file['content']
        else:
            return jsonify({"message": "File not found"}), 404

    else:
        return jsonify({"message": "Access Denied"}), 403


if __name__ == "__main__":
    app.run(debug=True)
