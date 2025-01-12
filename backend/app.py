# Import Flask server dependencies
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

# Importing necessary packages for Google OAuth
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/drive.file']

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

# Set the directory to save uploaded files
UPLOAD_FOLDER = 'backend/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
            out1, out2, out3 = summarize(file_path, aryn_api_key, anthropic_api_key)
            #print(summary)
            return jsonify({'message': 'File uploaded successfully', 'filePath': file_path, 'out1': json.loads(out1), 'out2': json.loads(out2), 'out3': json.loads(out3)}), 200
        except Exception as e:
            return jsonify({'error': 'Failed to process the file', 'details': str(e)}), 500
    else:
        return jsonify({'error': 'No file provided'}), 400
    


if __name__ == '__main__':
    app.run(debug=True, port=8000)

# import os
# import json
# from flask import Flask, redirect, request, session, url_for
# from google_auth_oauthlib.flow import Flow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# import google.auth.transport.requests

# # Flask setup
# app = Flask(__name__)
# app.secret_key = os.urandom(24)

# # Load your client secret JSON from Google Cloud
# CLIENT_SECRETS_FILE = "backend/client_secret.json"
# SCOPES = ['https://www.googleapis.com/auth/calendar.events']

# # Initialize OAuth flow
# flow = Flow.from_client_secrets_file(
#     CLIENT_SECRETS_FILE,
#     scopes=SCOPES,
#     redirect_uri='http://localhost:5000/callback'
# )

# @app.route('/')
# def index():
#     """Step 1: Show a link to log in."""
#     if 'credentials' in session:
#         return redirect(url_for('add_event'))
#     else:
#         return redirect(url_for('login'))

# @app.route('/login')
# def login():
#     """Step 2: Redirect to Google's OAuth 2.0 server."""
#     authorization_url, state = flow.authorization_url()
#     session['state'] = state
#     return redirect(authorization_url)

# @app.route('/callback')
# def callback():
#     """Step 3: Handle the OAuth 2.0 callback and fetch the access token."""
#     flow.fetch_token(authorization_response=request.url)
#     credentials = flow.credentials
#     session['credentials'] = credentials_to_dict(credentials)
#     return redirect(url_for('add_event'))

# @app.route('/add_event')
# def add_event():
#     """Step 4: Create an event on the user's Google Calendar."""
#     credentials = session.get('credentials')
#     if not credentials:
#         return redirect(url_for('login'))

#     try:
#         # Build the service
#         service = build('calendar', 'v3', credentials=credentials)

#         # Define the event
#         event = {
#             'summary': 'Sample Event',
#             'location': '123 Sample St, Sample City',
#             'description': 'A detailed event description',
#             'start': {
#                 'dateTime': '2025-01-12T09:00:00-07:00',
#                 'timeZone': 'America/Los_Angeles',
#             },
#             'end': {
#                 'dateTime': '2025-01-12T10:00:00-07:00',
#                 'timeZone': 'America/Los_Angeles',
#             },
#             'attendees': [
#                 {'email': 'sample@example.com'},
#             ],
#         }

#         # Insert the event into Google Calendar
#         event = service.events().insert(calendarId='primary', body=event).execute()

#         return f"Event created: {event.get('htmlLink')}"

#     except HttpError as error:
#         return f"An error occurred: {error}"

# # Helper function to store credentials in the session
# def credentials_to_dict(credentials):
#     """Convert credentials to a dictionary for session storage."""
#     return {
#         'token': credentials.token,
#         'refresh_token': credentials.refresh_token,
#         'token_uri': credentials.token_uri,
#         'client_id': credentials.client_id,
#         'client_secret': credentials.client_secret,
#         'scopes': credentials.scopes,
#     }

# if __name__ == '__main__':
#     app.run(debug=True)

