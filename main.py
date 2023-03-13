from flask import Flask, render_template
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

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
    values = read_sheet('', 'A10:D')
    return render_template('index.html', values=values)

def read_sheet(sheet_name: str, range: str):
    if not sheet_name:
        sheet_name = get_last_sunday()

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=f'{sheet_name}!{range}').execute()
    values = result.get('values', [])
    return values

def get_last_sunday():
    today = datetime.today()
    last_sunday = None
    if today.weekday() != 6: # Monday == 0 ... Sunday == 6
        days_from_sunday = today.weekday() + 1
        last_sunday = today - timedelta(days=days_from_sunday)
    else:
        last_sunday = today
    return last_sunday.strftime('%m%d')

def is_not_black(s):
    return bool(s and not s.isspace())

if __name__ == '__main__':
    app.run()
