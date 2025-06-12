from flask import Flask, request, render_template, send_from_directory, flash, redirect, url_for
from flask_mail import Mail, Message
import mysql.connector
import os
import secrets

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static',
    static_url_path='')

# Set secret key for session management
app.secret_key = secrets.token_hex(16)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'ulhaqhassan2@gmail.com'
app.config['MAIL_PASSWORD'] = 'fffy lkiy rtby pbuq'  # Updated App Password
app.config['MAIL_DEFAULT_SENDER'] = 'ulhaqhassan2@gmail.com'
app.config['MAIL_MAX_EMAILS'] = 5
app.config['MAIL_ASCII_ATTACHMENTS'] = False
app.config['MAIL_SUPPRESS_SEND'] = False

mail = Mail(app)

# Enable debug mode for development
app.debug = True

# Database configuration
db = mysql.connector.connect(
    host="localhost",
    user="mural_user",
    password="Mural@123",
    database="mural_db"
)

cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS mural_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    dimensions VARCHAR(100),
    art_type VARCHAR(100),
    location TEXT,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('service.html')

@app.route('/about')
def about():
    return render_template('aboutus.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get form data
        first_name = request.form['fname']
        last_name = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']
        dimensions = request.form['dimensions']
        art_type = request.form['art_type']
        location = request.form['location']
        details = request.form['details']

        # Save to database
        query = """
        INSERT INTO mural_orders 
        (first_name, last_name, email, phone, dimensions, art_type, location, details)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, email, phone, dimensions, art_type, location, details))
        db.commit()

        # Send confirmation email
        msg = Message(
            subject=f"Thank you for your mural order, {first_name}!",
            recipients=[email]
        )
        
        # Create HTML email body
        msg.html = f"""
        <html>
            <body>
                <p>Hi {first_name},</p>
                
                <p>Thank you for placing your custom mural order with Mr Curly! 🎨✨</p>
                
                <p>We've received the following details from you:</p>
                
                <p>--------------------------------------------------<br>
                🧑 Name: {first_name} {last_name}<br>
                📧 Email: {email}<br>
                📞 Phone: {phone}<br>
                📍 Location: {location}<br>
                📐 Dimensions: {dimensions}<br>
                🖌️ Art Type: {art_type}<br>
                🎨 Mural Details / Theme:<br>
                {details}<br>
                --------------------------------------------------</p>
                
                <p>Our team will get back to you shortly to confirm your order and discuss the next steps. 
                If you have any urgent questions, feel free to reply to this email.</p>
                
                <p>Looking forward to bringing your walls to life!</p>
                
                <p>Warm regards,<br>
                <strong>Team Mr Curly</strong><br>
                📩 mr.curly@example.com<br>
                🌐 www.mrcurly.com</p>
            </body>
        </html>
        """
        
        try:
            mail.send(msg)
            print(f"Email sent successfully to {email}")
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            raise
        
        flash('Your order has been submitted successfully! Please check your email for confirmation.', 'success')
        return redirect(url_for('services'))
        
    except Exception as e:
        print(f"Error in submit route: {str(e)}")
        flash('There was an error submitting your order. Please try again.', 'error')
        return redirect(url_for('services'))

if __name__ == '__main__':
    app.run(debug=True)
