from flask import Flask, render_template
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'config/credentials.json'
SPREADSHEET_ID = '1VtGRDekqg3spOTy9sNxwdewHzYn2yPjB4n6nt4OqYfo'

creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)

@app.route('/')
def home():
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range='0305!A10:D35').execute()
    values = result.get('values', [])
    return render_template('index.html', values=values)

if __name__ == '__main__':
    app.run()
