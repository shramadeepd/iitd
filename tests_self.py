import pytest
from io import BytesIO
import base64
from PIL import Image
from flask import json
from app import app  


# function to convert image to base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string


# Fixture to provide a test client for Flask app
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Test the /api/get-text route for successful text extraction
def test_get_text_success(client):
    
    image_path = '1.jpg'  # image path
    base64_image = encode_image_to_base64(image_path)

    # Created a request payload with the base64 image
    payload = {
        'base64_image': base64_image
    }

    # Sent a POST request to the API
    response = client.post('/api/get-text', json=payload)

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert 'text' in json_data['result']


# Test the /api/get-text route for missing base64_image
def test_get_text_missing_image(client):
    # Create a request payload without base64_image
    payload = {}

    # Sent a POST request to the API
    response = client.post('/api/get-text', json=payload)

    # Assert the response status code and error message
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['success'] is False
    assert json_data['error']['message'] == 'base64_image is required.'


# Test the /api/get-text route for invalid base64_image
def test_get_text_invalid_image(client):
    # Create a request payload with an invalid base64 image
    payload = {
        'base64_image': 'invalid_base64_string'
    }


    response = client.post('/api/get-text', json=payload)

    # Assert the response status code and error message
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['success'] is False
    assert json_data['error']['message'] == 'Invalid base64_image.'


# Test the /api/get-bboxes route for successful bbox extraction
def test_get_bboxes_success(client):
    # Load a sample image and encode it as base64
    image_path = '1.jpg'  # Replace with a valid image path
    base64_image = encode_image_to_base64(image_path)

    # Create a request payload with the base64 image and bbox_type
    payload = {
        'base64_image': base64_image,
        'bbox_type': 'word'
    }

    # Send a POST request to the API
    response = client.post('/api/get-bboxes', json=payload)

    # Assert the response status code and JSON response
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert 'bboxes' in json_data['result']
    assert isinstance(json_data['result']['bboxes'], list)


# Test the /api/get-bboxes route for missing base64_image
def test_get_bboxes_missing_image(client):
    # Create a request payload without base64_image
    payload = {
        'bbox_type': 'word'
    }

    # Send a POST request to the API
    response = client.post('/api/get-bboxes', json=payload)

    # Assert the response status code and error message
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['success'] is False
    assert json_data['error']['message'] == 'base64_image is required.'


# Test the /api/get-bboxes route for invalid bbox_type
def test_get_bboxes_invalid_bbox_type(client):
    # Load a sample image and encode it as base64
    image_path = '1.jpg'  # Replace with a valid image path
    base64_image = encode_image_to_base64(image_path)

    # Create a request payload with the base64 image and invalid bbox_type
    payload = {
        'base64_image': base64_image,
        'bbox_type': 'invalid_type'
    }

    # Send a POST request to the API
    response = client.post('/api/get-bboxes', json=payload)

    # Assert the response status code and error message
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['success'] is False
    assert json_data['error']['message'] == 'Invalid bbox_type.'


# Test the /api/get-bboxes route for invalid base64_image
def test_get_bboxes_invalid_image(client):
    # Create a request payload with an invalid base64 image
    payload = {
        'base64_image': 'invalid_base64_string',
        'bbox_type': 'word'
    }

    # Send a POST request to the API
    response = client.post('/api/get-bboxes', json=payload)

    # Assert the response status code and error message
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['success'] is False
    assert json_data['error']['message'] == 'Invalid base64_image.'
