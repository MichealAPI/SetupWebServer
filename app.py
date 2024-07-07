from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

SECRET_URI = os.getenv('SECRET_URI')

app = Flask(__name__)
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
# GET mapping '/'
#
@app.route('/<path:path>', methods=['GET'])
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
