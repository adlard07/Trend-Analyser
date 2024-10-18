from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from flask import Flask, request
import webbrowser
import threading
import json
import os


class GoogleDriveClient:
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 
              'https://www.googleapis.com/auth/spreadsheets.readonly']
    REDIRECT_URI = 'http://127.0.0.1:5500/callback'
    TOKEN_FILE = 'token.json'
    CREDENTIALS_FILE = 'credentials.json'

    def __init__(self):
        self.authorization_code = None
        self.creds = None
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        """Set up Flask routes dynamically."""
        @self.app.route('/callback')
        def callback():
            """OAuth callback to capture the authorization code."""
            self.authorization_code = request.args.get('code')
            return "Authorization successful! You can close this window now."

    def start_server(self):
        """Start the Flask server."""
        self.app.run(host='127.0.0.1', port=5500)

    def get_credentials(self):
        """Handles the OAuth flow and retrieves the credentials."""
        flow = Flow.from_client_secrets_file(
            self.CREDENTIALS_FILE, self.SCOPES, redirect_uri=self.REDIRECT_URI)
        
        auth_url, _ = flow.authorization_url(prompt='consent')
        server_thread = threading.Thread(target=self.start_server)
        server_thread.daemon = True
        server_thread.start()

        webbrowser.open(auth_url)
        while self.authorization_code is None:
            pass

        flow.fetch_token(code=self.authorization_code)
        self.creds = flow.credentials
        self.save_credentials()

    def save_credentials(self):
        """Save the OAuth credentials to a file."""
        with open(self.TOKEN_FILE, 'w') as token:
            token.write(self.creds.to_json())

    def load_credentials(self):
        """Load the credentials from the token file, refreshing them if necessary."""
        if os.path.exists(self.TOKEN_FILE):
            self.creds = Credentials.from_authorized_user_file(self.TOKEN_FILE, self.SCOPES)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
                self.save_credentials()
            else:
                self.get_credentials()

    def fetch_sheets(self):
        """Fetch a list of Google Sheets from the Drive account."""
        if not self.creds:
            self.load_credentials()

        try:
            drive_service = build('drive', 'v3', credentials=self.creds)
            results = drive_service.files().list(
                q="mimeType='application/vnd.google-apps.spreadsheet'",
                fields="files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No spreadsheets found.')
                return

            print('Spreadsheets:')
            for item in items:
                print(f"Name: {item['name']}", f"ID: {item['id']}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def remove_token(self):
        """Remove the existing token file if it exists."""
        if os.path.exists(self.TOKEN_FILE):
            os.remove(self.TOKEN_FILE)

    def fetch_sheet_content(self, sheet_id, range_name='Sheet1!A1:Z1000'):
        """Fetch the content of a specific Google Sheet."""
        if not self.creds:
            self.load_credentials()

        try:
            sheets_service = build('sheets', 'v4', credentials=self.creds)
            sheet = sheets_service.spreadsheets()
            result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
            values = result.get('values', [])

            if not values:
                print('No data found in the specified sheet.')
                return

            print('Sheet content:')
            for row in values:
                print(row)

            return values

        except Exception as e:
            print(f"An error occurred while fetching sheet content: {e}")

if __name__ == '__main__':
    google_drive_client = GoogleDriveClient()
    google_drive_client.remove_token()
    google_drive_client.fetch_sheets()
    
    sheet_id = '1vKV48aE9EzlEyISztKtzmF8xJV0HT5v3zU1NKurC1tM'
    sheet_content = google_drive_client.fetch_sheet_content(sheet_id)