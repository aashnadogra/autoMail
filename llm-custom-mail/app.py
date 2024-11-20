from flask import Flask, redirect, url_for, session, request, render_template, flash
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os
import base64
import csv
from werkzeug.utils import secure_filename
from groq import Groq
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()


app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')  # Set a default for development

CLIENT_SECRETS_FILE = os.getenv('GOOGLE_CLIENT_SECRETS', 'client_secret.json')

client = os.getenv(Groq(api_key='GROQ_API_KEY'))



# Set OpenAI API key from environment variable



SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/gmail.send']
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def create_flow():
    return Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('callback', _external=True)
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    flow = create_flow()
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)

@app.route('/callback')
def callback():
    flow = create_flow()
    flow.fetch_token(authorization_response=request.url)
    session['credentials'] = credentials_to_dict(flow.credentials)
    return redirect(url_for('sheet_input'))

@app.route('/sheet_input')
def sheet_input():
    if 'credentials' not in session:
        return redirect(url_for('login'))
    return render_template('sheet_input.html')

@app.route('/send_emails', methods=['POST'])
def send_emails():
    if 'credentials' not in session:
        return redirect(url_for('login'))

    credentials = Credentials(**session['credentials'])
    email_column = request.form['email_column']
    user_prompt = request.form['user_prompt']

    sheet_id = request.form.get('sheet_id')
    if sheet_id:
        # Google Sheets logic
        try:
            service = build('sheets', 'v4', credentials=credentials)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=sheet_id, range='Sheet1').execute()
            values = result.get('values', [])

            if not values:
                flash("No data found in Google Sheet.")
                return redirect(url_for('sheet_input'))

            headers = values[0]
            if email_column not in headers:
                flash(f"Column '{email_column}' not found in Google Sheet.")
                return redirect(url_for('sheet_input'))

            emails = [dict(zip(headers, row)) for row in values[1:]]

        except Exception as e:
            flash(f"Error accessing Google Sheet: {e}")
            return redirect(url_for('sheet_input'))

    else:
        # CSV data handling
        uploaded_file = request.files['file']
        if not uploaded_file or not uploaded_file.filename.endswith('.csv'):
            flash("Please upload a valid CSV file.")
            return redirect(url_for('sheet_input'))

        file_path = os.path.join('uploads', secure_filename(uploaded_file.filename))
        uploaded_file.save(file_path)

        try:
            emails = []
            with open(file_path, mode='r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                headers = reader.fieldnames
                if not headers or email_column not in headers:
                    flash(f"Column '{email_column}' not found in CSV file. Available columns: {headers}")
                    return redirect(url_for('sheet_input'))

                for row in reader:
                    emails.append(row)

        except Exception as e:
            flash(f"Error reading CSV file: {e}")
            return redirect(url_for('sheet_input'))

    # Generate and send personalized emails
    for row in emails:
        email_address = row.get(email_column)
        email_content = generate_email_content(user_prompt, row)

        try:
            send_gmail_message(credentials, email_address, "Custom Email", email_content)
        except Exception as e:
            print(f"Failed to send email to {email_address}: {e}")

    flash("Emails sent successfully!")
    return redirect(url_for('sheet_input'))




def generate_email_content(prompt_template, row_data):
    # Format the prompt with the provided row data
    prompt = prompt_template.format(**row_data)

    

    try:
        # Call Groq API with the chat.completions.create method
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            max_tokens=500
        )
        # Return the generated content from the API response
        return response.choices[0].message.content.strip()

    except Exception as e:
        # General error logging for any API errors
        print(f"Error generating email content: {e}")
        return "We're sorry, but we couldn't generate your email content due to an unexpected error."
    


def send_gmail_message(credentials, to_email, subject, body_text):
    service = build('gmail', 'v1', credentials=credentials)
    message = {
        'raw': base64.urlsafe_b64encode(
            f"From: me\nTo: {to_email}\nSubject: {subject}\n\n{body_text}".encode('utf-8')
        ).decode('utf-8')
    }
    try:
        service.users().messages().send(userId="me", body=message).execute()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

if __name__ == "__main__":
    app.run(debug=True)
