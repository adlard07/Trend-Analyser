import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from flask import Flask, request
import webbrowser
import threading
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GoogleDriveClient:
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 
              'https://www.googleapis.com/auth/spreadsheets.readonly']
    REDIRECT_URI = 'http://127.0.0.1:5500/callback'
    TOKEN_FILE = 'backend/data_ingestion/token.json'
    CREDENTIALS_FILE = 'backend/data_ingestion/credentials.json'

    def __init__(self):
        self.authorization_code = None
        self.creds = None
        self.app = Flask(__name__)
        self.setup_routes()
        logger.info("GoogleDriveClient initialized")

    def setup_routes(self):
        """Set up Flask routes dynamically."""
        @self.app.route('/callback')
        def callback():
            """OAuth callback to capture the authorization code."""
            self.authorization_code = request.args.get('code')
            logger.info("Authorization code received")
            return "Authorization successful! You can close this window now."

    def start_server(self):
        """Start the Flask server."""
        try:
            self.app.run(host='127.0.0.1', port=5500)
        except Exception as e:
            logger.error(f"Failed to start Flask server: {str(e)}")
            raise

    def get_credentials(self):
        """Handles the OAuth flow and retrieves the credentials."""
        try:
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
            logger.info("Credentials obtained successfully")
        except Exception as e:
            logger.error(f"Failed to get credentials: {str(e)}")
            raise

    def save_credentials(self):
        """Save the OAuth credentials to a file."""
        try:
            with open(self.TOKEN_FILE, 'w') as token:
                token.write(self.creds.to_json())
            logger.info("Credentials saved successfully")
        except Exception as e:
            logger.error(f"Failed to save credentials: {str(e)}")
            raise

    def load_credentials(self):
        """Load the credentials from the token file, refreshing them if necessary."""
        try:
            if os.path.exists(self.TOKEN_FILE):
                self.creds = Credentials.from_authorized_user_file(self.TOKEN_FILE, self.SCOPES)
            
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                    self.save_credentials()
                else:
                    self.get_credentials()
            logger.info("Credentials loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load credentials: {str(e)}")
            raise

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
                logger.info("No sheets found")
                return []

            sheets = [{"name": item['name'], "id": item['id']} for item in items]
            logger.info(f"Successfully fetched {len(sheets)} sheets")
            return sheets

        except Exception as e:
            logger.error(f"An error occurred while fetching sheets: {str(e)}")
            raise

    def remove_token(self):
        """Remove the existing token file if it exists."""
        try:
            if os.path.exists(self.TOKEN_FILE):
                os.remove(self.TOKEN_FILE)
                logger.info("Token file removed successfully")
            else:
                logger.info("No token file to remove")
        except Exception as e:
            logger.error(f"Failed to remove token file: {str(e)}")
            raise

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
                logger.info('No data found in the specified sheet.')
                return []

            logger.info(f"Successfully fetched content from sheet: {sheet_id}")
            return values

        except Exception as e:
            logger.error(f"An error occurred while fetching sheet content: {str(e)}")
            raise

if __name__ == '__main__':
    try:
        google_drive_client = GoogleDriveClient()
        google_drive_client.remove_token()
        sheets = google_drive_client.fetch_sheets()
        print(f"Fetched {len(sheets)} sheets")
        
        sheet_id = '1vKV48aE9EzlEyISztKtzmF8xJV0HT5v3zU1NKurC1tM'
        sheet_content = google_drive_client.fetch_sheet_content(sheet_id)
        print(f"Fetched {len(sheet_content)} rows from the sheet")
    except Exception as e:
        logger.critical(f"An unhandled exception occurred: {str(e)}")
        print(f"A critical error occurred. Please check the log file for details.")