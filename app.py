from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests

load_dotenv()

app = Flask(__name__)

# Enable CORS
# CORS(app, resources={r"/*": {"origins": ["https://micro-chat-bot-by-somy.vercel.app"]}})
CORS(app, resources={r"/*": {"origins": ["https://micro-chat-bot-by-somy.vercel.app"]}})


# Handle preflight (OPTIONS) requests for CORS
""" @app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://micro-chat-bot-by-somy.vercel.app')  # Adjust origin as needed
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response
 """
# Set up bcrypt for password hashing
bcrypt = Bcrypt(app)
kinky = os.getenv('kinky')
# Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///credentials.db" # Replace with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

# Create database tables (if they don't exist)
# @app.before_first_request
""" def initDB():
    db.create_all() """

# Opening index.html
@app.route('/')
def openLogin():
    return render_template("index.html")

# Login route
@app.route('/api/login', methods=["POST"])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid username or password"}), 400

# Sign-up route
@app.route('/api/sign-up', methods=["POST"])
def signUp():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    hashedPass = bcrypt.generate_password_hash(password).decode('utf-8')
    
    try:
        # Add user to the database
        new_user = User(username=username, password=hashedPass)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Signup successful"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Username already exists"}), 400

# Opening chat bot
@app.route('/micro-chat-bot', methods=['GET'])
def chat_bot():
    return render_template('micro-chat-bot.html')

# Opening reset password form
@app.route('/reset-password')
def resetPass():
    return render_template('reset-password.html')

# Storing new password
@app.route('/api/resetpassword', methods=['POST'])
def reset():
    resetUser = request.json.get('resetUsername')
    resetPass = request.json.get('resetPassword')

    if not resetUser or not resetPass:
        return jsonify({"message": "Username and password are required"}), 400

    hashedPass = bcrypt.generate_password_hash(resetPass).decode('utf-8')
    try:
        user = User.query.filter_by(username=resetUser).first()
        if user:
            user.password = hashedPass
            db.session.commit()
            return jsonify({"message": "Password reset successful."}), 200
        return jsonify({"message": "Username does not exist!"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred during password reset."}), 500

# Response fetch from external API (Chatbot)
url = "https://openrouter.ai/api/v1/chat/completions"

@app.route('/api/chat', methods=["POST"])
def chat():
    data = request.json
    userQuery = data.get('query', '').strip()

    if not userQuery:
        return jsonify({"response": "Please provide a query"}), 400

    headers = {
        "Authorization": f"Bearer {kinky}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": userQuery}]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        botResponse = response.json()["choices"][0]["message"]["content"]
        return jsonify({"response": botResponse}), 200

    except requests.exceptions.RequestException as e:
        print(f"Request to OpenAI API failed: {e}")
        return jsonify({"response": "Failed to fetch response. Please try again later."}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
