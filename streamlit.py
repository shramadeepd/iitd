import streamlit as st
import requests
import base64
from PIL import Image
import io

# Function to convert image to base64
def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

# Function to send request to API
def send_request_to_api(api_url, base64_image, bbox_type=None):
    if api_url.endswith('/api/get-text'):
        data = {"base64_image": base64_image}
    elif api_url.endswith('/api/get-bboxes'):
        data = {
            "base64_image": base64_image,
            "bbox_type": bbox_type
        }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, json=data, headers=headers)

    
    st.write(f"Status Code: {response.status_code}")
    

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        st.error("Failed to decode JSON response from the API.")
        return None

st.title("Image Upload and API Tester")

# Image upload component
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Dropdown to select which API to hit
api_selection = st.selectbox("Choose API to hit", ["/api/get-text", "/api/get-bboxes"])

# Only show bbox_type input if /api/get-bboxes is selected
bbox_type = None
if api_selection == "/api/get-bboxes":
    bbox_type = st.selectbox("Choose bounding box type", ["word", "line", "paragraph", "block", "page"])



# Button to send the image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img = encode_image_to_base64(image)
    
    
    base64_image = encode_image_to_base64(image)
    
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    
    api_url = f"http://127.0.0.1:8000{api_selection}" 

    if st.button("Send to API"):
        # Sends the request to the Flask API
        response_data = send_request_to_api(api_url, base64_image, bbox_type=bbox_type)
        

        
        if response_data:
            st.json(response_data)
        else:
            st.error("Error in API response.")
