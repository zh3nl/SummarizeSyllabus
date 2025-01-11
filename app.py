from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

# Set the directory to save uploaded files
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route to render the upload form
@app.route('/')
def index():
    return render_template('summarizesyllabus/public/index.html')

if __name__ == '__main__':
    app.run(debug=True)
