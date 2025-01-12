# Import Flask server dependencies
from flask import Flask, request, jsonify, redirect, session, url_for
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

# Importing necessary packages for Google OAuth
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
CLIENT_SECRET_FILE = 'backend/client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
REDIRECT_URI = 'http://localhost:8000/callback'

# Importing necessary packages for Aryn DocParse and Claude
import anthropic
from aryn_sdk.partition import partition_file
import json
from pydantic import BaseModel

# Importing functions for summarization
from claude import format_content, printout, summarize

# Importing API keys from environment variable
from dotenv import load_dotenv
load_dotenv()
aryn_api_key = os.getenv('aryn_API_KEY')
anthropic_api_key = os.getenv('anthropic_API_KEY')

# Initializing Flask server
app = Flask(__name__)
CORS(app)

app.secret_key = os.urandom(24)

# Set the directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
summary = [
    {
        "image_title": "Lectures",
        "image_description": "{\n      'summary': 'CS 122A/EECS 116 Lecture',\n      'location': 'HSLH 100A',\n      'description': 'Introduction to Data Management lecture',\n      'start': {\n        'dateTime': '2025-01-07T11:00:00-08:00',\n        'timeZone': 'America/Los_Angeles'\n      },\n      'end': {\n        'dateTime': '2025-01-07T12:20:00-08:00',\n        'timeZone': 'America/Los_Angeles'\n      },\n      'recurrence': [\n        'RRULE:FREQ=WEEKLY;BYDAY=TU,TH;UNTIL=20250321T235959Z'\n      ],\n      'attendees': [],\n      'reminders': {\n        'useDefault': false,\n        'overrides': [\n          {'method': 'email', 'minutes': 1440},\n          {'method': 'popup', 'minutes': 10}\n        ]\n      }\n    }"
    }]

def credentials_to_dict(credentials):
    """Converts credentials to a dictionary."""
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }

@app.route('/login')
def login():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI)
    
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true')
    
    session['state'] = state  # Store the state in the session for CSRF protection
    
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    # Get the authorization response and state from the URL
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI)
    flow.fetch_token(authorization_response=request.url)
    
    # Store the credentials in session
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    if 'credentials' not in session:
        return jsonify({'error': 'User not authenticated'}), 401
    
    # Retrieve credentials from the session
    credentials = session['credentials']
    
    # Build the Google Calendar service
    service = build('calendar', 'v3', credentials=credentials)
    
    # Example event data (replace with your actual event data)
    for i in summary[0]:
       
       event = service.events().insert(calendarId='primary', body=i['image_description']).execute() 
    return redirect(url_for('dashboard'))  # Redirect back to the dashboard page

# Route to render the upload form
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            summary = summarize(file_path, aryn_api_key, anthropic_api_key)
            #print(summary)
            return jsonify({'message': 'File uploaded successfully', 'filePath': file_path, 'summary':summary }), 200
        except Exception as e:
            return jsonify({'error': 'Failed to process the file', 'details': str(e)}), 500
    else:
        return jsonify({'error': 'No file provided'}), 400
    


if __name__ == '__main__':
    app.run(debug=True, port=8000)