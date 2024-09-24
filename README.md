# IITD Internship Full stack assignment

# API Tester for Tesseract OCR Server Assignment

## Setup and run locally
Clone this repository:
```
git clone https://github.com/shramadeepd/iitd.git
```

Move into the newly created folder:
```
cd iitd
```

Install the dependencies (using a virtual environment is recommended):
```
pip install -r requirements.txt
```
Start the server :
```
python app.py
```
app.py is the main server file , that contains all the apis 

Start the frontend in a new terminal :
```
streamlit run streamlit.py
```
In the streamlit app the image can be directly uploaded and then the api can be choosen and the response is shown back 

Test that i have written using pytest :
```
pytest tests_self.py
```
Test mentioned in repo has version issue with tesseract as it was not supporting the python3 so ihave implemented the test with pytesseract and tried to achieve the same output :
```
python test.py
```
Docker image for the code :
```
docker pull shramadeepd/flask-ocr-app:v1.0
```

