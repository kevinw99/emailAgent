import os
import pathlib
from flask import Flask, render_template, request, redirect, url_for, session
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import google.auth.exceptions
import pickle
import certifi
import os

# os.environ['SSL_CERT_FILE'] = certifi.where()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CLIENT_SECRETS_FILE = 'client_secret.json'
TOKEN_FILE = 'token.pickle'

@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    return "Gmail authentication complete! Ready to scan emails. <a href='/scan'>Scan now</a>"

@app.route('/authorize')
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    # Save credentials in session (for demo; use secure storage in production)
    session['credentials'] = credentials_to_dict(credentials)
    # Also save to file for reuse
    with open(TOKEN_FILE, 'wb') as token:
        pickle.dump(credentials, token)
    return redirect(url_for('index'))

@app.route('/scan')
def scan():
    creds = None
    if 'credentials' in session:
        from google.oauth2.credentials import Credentials
        creds = Credentials(**session['credentials'])
    elif os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            return redirect(url_for('authorize'))
    try:
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
        email_list = []
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = msg_data.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
            from_addr = next((h['value'] for h in headers if h['name'] == 'From'), '(No From)')
            email_list.append({'subject': subject, 'from': from_addr})
        return render_template('scan.html', emails=email_list)
    except google.auth.exceptions.RefreshError:
        return redirect(url_for('authorize'))
    except Exception as e:
        return f"Error: {e}"

def credentials_to_dict(creds):
    return {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }

if __name__ == '__main__':
    app.run(debug=True)
