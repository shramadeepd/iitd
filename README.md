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
python tesseract.py
```
Start the frontend in a new terminal :
```
streamlit run streamlit.py
```
Test that i have written using pytest :
```
python test_self.py
```
Test mentioned in repo has version issue with tesseract as it was not supporting the python3 so ihave implemented the test with pytesseract and tried to achieve the same output :
```
python test.py
```


