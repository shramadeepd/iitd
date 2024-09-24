from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
import pytesseract
from pytesseract import Output

app = Flask(__name__)

# function to decode base64 image 
def decode_base64_image(base64_string):
    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data))
        return image
    except Exception as e:
        return None

# Route to extract text from image
@app.route('/api/get-text', methods=['POST'])
def get_text():
    try:
        data = request.json
        base64_image = data.get('base64_image')

        if not base64_image:
            return jsonify({"success": False, "error": {"message": "base64_image is required."}}), 400

        image = decode_base64_image(base64_image)
        if image is None:
            return jsonify({"success": False, "error": {"message": "Invalid base64_image."}}), 400

        text = pytesseract.image_to_string(image)

        return jsonify({"success": True, "result": {"text": text}})
    
    except Exception as e:
        return jsonify({"success": False, "error": {"message": str(e)}}), 500

# Route to extract bounding boxes from image
@app.route('/api/get-bboxes', methods=['POST'])
def get_bboxes():
    try:
        data = request.json
        base64_image = data.get('base64_image')
        bbox_type = data.get('bbox_type')

        if not base64_image:
            return jsonify({"success": False, "error": {"message": "base64_image is required."}}), 400
        if bbox_type not in ['word', 'line', 'paragraph', 'block', 'page']:
            return jsonify({"success": False, "error": {"message": "Invalid bbox_type."}}), 400

        image = decode_base64_image(base64_image)
        if image is None:
            return jsonify({"success": False, "error": {"message": "Invalid base64_image."}}), 400

        
        ocr_data = pytesseract.image_to_data(image, output_type=Output.DICT)

    
        bboxes = []
        for i in range(len(ocr_data['level'])):
            if ocr_data['level'][i] == get_level_from_type(bbox_type):
                bbox = {
                    "x_min": ocr_data['left'][i],
                    "y_min": ocr_data['top'][i],
                    "x_max": ocr_data['left'][i] + ocr_data['width'][i],
                    "y_max": ocr_data['top'][i] + ocr_data['height'][i],
                }
                bboxes.append(bbox)

        
        return jsonify({"success": True, "result": {"bboxes": bboxes}})

    except Exception as e:
        return jsonify({"success": False, "error": {"message": str(e)}}), 500

# function to map bbox_type to pytesseract level
def get_level_from_type(bbox_type):
    bbox_type_to_level = {
        'word': 5,
        'line': 4,
        'paragraph': 3,
        'block': 2,
        'page': 1,
    }
    return bbox_type_to_level.get(bbox_type)

if __name__ == '__main__':
    app.run(debug=True,port=8000)
