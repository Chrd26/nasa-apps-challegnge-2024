import sys
import os
sys.path.insert(0, os.path.abspath('./controllers/'))
from results import Results
from flask import Flask
from flask import render_template, request

# Wheel might fail due to cython
# Use the following: 
# https://discuss.python.org/t/getting-requirements-to-build-wheel-did-not-run-successfully-exit-code-1/30365

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/get-info', methods=['POST'])
async def ShowInfo():
    location = request.form["location-input"]

    if not location:
        return render_template('index.html')

    results = Results(location)

    if not results.isLocationFound:
        return render_template('index.html')

    return render_template('result.html', name_location = location)

if __name__ == '__main__':
    run(app)
