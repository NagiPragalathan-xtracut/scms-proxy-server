# test/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'  # Gmail SMTP server
SMTP_PORT = 587  # TLS port
SMTP_USERNAME = 'nagi@xtracut.com'
SMTP_PASSWORD = 'ihyv sfqb ablz iogi'

def generate_otp(length=6):
    """Generate a random OTP of specified length"""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(email, otp):
    """Send OTP to the specified email address"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = email
        msg['Subject'] = "SCMS Journal Management System - OTP Verification"

        body = f"""
Dear User,

Thank you for using the SCMS Journal Management System.

Your One-Time Password (OTP) for verification is: {otp}

This OTP is valid for 5 minutes and should not be shared with anyone.

If you did not request this OTP, please ignore this email or contact our support team.

Best regards,
SCMS Journal Management System Team
        """
        
        msg.attach(MIMEText(body, 'plain'))

        # Create SMTP session
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Using TLS as specified in smtp_auth
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(SMTP_USERNAME, email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

@app.route('/generate-otp', methods=['POST'])
def generate_and_send_otp():
    try:
        # Get email from request
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({'error': 'Email is required'}), 400

        email = data['email']
        
        # Generate OTP
        otp = generate_otp()
        
        # Send OTP via email
        if send_otp_email(email, otp):
            return jsonify({
                'status': 'success',
                'message': 'OTP sent successfully',
                'otp': otp  # In production, you should not return the OTP in the response
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to send OTP'
            }), 500

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
