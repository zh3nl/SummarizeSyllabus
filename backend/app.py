# Import Flask server dependencies
from flask import Flask, request, jsonify, redirect, session, url_for
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from google.oauth2.credentials import Credentials

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
outglobal = None

def credentials_from_dict(credentials_dict):
    return Credentials(
        token=credentials_dict['token'],
        refresh_token=credentials_dict['refresh_token'],
        token_uri=credentials_dict['token_uri'],
        client_id=credentials_dict['client_id'],
        client_secret=credentials_dict['client_secret'],
        scopes=credentials_dict['scopes']
    )

# Importing necessary packages for Google OAuth
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
REDIRECT_URI = 'http://localhost:8000/callback'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

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

app.secret_key = "supersecretkey"

# Set the directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
summary = [
    {
        "image_title": "Lectures",
        "image_description": {
            "summary": "CS 122A/EECS 116 Lecture",
            "location": "HSLH 100A",
            "description": "Introduction to Data Management lecture",
            "start": {
                "dateTime": "2025-01-07T11:00:00-08:00",
                "timeZone": "America/Los_Angeles"
            },
            "end": {
                "dateTime": "2025-01-07T12:20:00-08:00",
                "timeZone": "America/Los_Angeles"
            },
            "recurrence": [
                "RRULE:FREQ=WEEKLY;BYDAY=TU,TH;UNTIL=20250321T235959Z"
            ],
            "attendees": [],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 1440},
                    {"method": "popup", "minutes": 10}
                ]
            }
        }
    }
]

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

@app.route("/dashboard")
def dashboard():
    return "This is the dashboard."

@app.route('/callback')
def callback():
    global outglobal
    # 1. Check if user DID upload a file
    # if 'out1' not in session:
    #     return jsonify({'error': 'No processed data available'}), 400

    # 2. Finish the OAuth flow
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        state=session['state']  # optional but recommended to match the state
    )
    flow.fetch_token(authorization_response=request.url)

    # 3. Convert credentials to dict and store in session
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    if 'credentials' not in session:
        return jsonify({'error': 'User not authenticated'}), 401

    creds = credentials_from_dict(session['credentials'])

    # 4. Build the service
    service = build('calendar', 'v3', credentials=creds)

    # 5. Parse events out of session['out1']
    out1_json_str = outglobal
    print(outglobal)
    events = json.loads(out1_json_str)
    for event_obj in events:
        image_desc_str = event_obj["image_description"]
        # Convert single quotes to double quotes
        image_desc_str = image_desc_str.replace("'", '"')
        image_desc_dict = json.loads(image_desc_str)
        if 'attendees' in image_desc_dict:
            image_desc_dict['attendees'] = None
        service.events().insert(
            calendarId='primary',
            body=image_desc_dict
        ).execute()
    outglobal = None
    # 6. Redirect user to front-end or show success
    return redirect('http://localhost:3000/courseinfo')


# Route to render the upload form
@app.route('/upload', methods=['POST'])
def upload():
    global outglobal
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            out1, out2, out3 = summarize(file_path, aryn_api_key, anthropic_api_key)
            outglobal = out1
            session['out1'] = out1
            return jsonify({'message': 'File uploaded successfully', 'filePath': file_path, 'out1': json.loads(out1), 'out2': json.loads(out2), 'out3': json.loads(out3) }), 200
        except Exception as e:
            return jsonify({'error': 'Failed to process the file', 'details': str(e)}), 500
    else:
        return jsonify({'error': 'No file provided'}), 400



if __name__ == '__main__':
    app.run(debug=True, port=8000)
message.txt
7 KB