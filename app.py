from flask import Flask, request
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
from libs import get_data
import io

app = Flask(__name__)

CORS(app)

model = YOLO("best.pt")

@app.route("/detect", methods=["POST"])
def detect():
    try:
        if 'file' not in request.files or not request.files['file']:
            return {"message": "파일을 업로드 하세요."}, 400

        file = request.files['file']

        image = Image.open(io.BytesIO(file.read()))

        result = model(source=image)
        items = [box.data[0].tolist() for item in result for box in item.boxes]
        for item in items:
            item.append(model.names[int(item[-1])])

        return items
    except Exception as e:
        return {"message", str(e)}, 500

@app.route("/crawler", methods=["POST"])
def crawler():
    data = request.json
    selector = data['linkSelector'], data['titleSelector'], data['dateSelector'], data['contentSelector']

    items = get_data(data['url'], selector, data['urlPrefix'], data['keywords'])

    return items