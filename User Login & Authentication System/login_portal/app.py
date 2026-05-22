from flask import Flask, request, jsonify, session, send_from_directory
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import mysql.connector

# ================= APP CONFIG =================
app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = "super_secret_key"

CORS(app, supports_credentials=True)

bcrypt = Bcrypt(app)

# ================= DATABASE CONNECTION =================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@1432",
    database="login_portal"
)

cursor = db.cursor(dictionary=True)

# ================= FRONTEND ROUTES =================
# ================= FRONTEND ROUTES =================

@app.route('/')
def home():
    return send_from_directory('static', 'login.html')


@app.route('/login.html')
def login_html():
    return send_from_directory('static', 'login.html')


@app.route('/register.html')
def register_html():
    return send_from_directory('static', 'register.html')


@app.route('/dashboard.html')
def dashboard_html():
    return send_from_directory('static', 'dashboard.html')
# ================= REGISTER =================
@app.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({
            "message": "All fields are required"
        }), 400

    # CHECK EXISTING USER
    cursor.execute(
        "SELECT * FROM users WHERE email=%s OR username=%s",
        (email, username)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({
            "message": "User already exists"
        }), 409

    # HASH PASSWORD
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # INSERT USER
    query = """
        INSERT INTO users (username, email, password)
        VALUES (%s, %s, %s)
    """

    values = (username, email, hashed_password)

    cursor.execute(query, values)
    db.commit()

    return jsonify({
        "message": "Registration successful"
    }), 201


# ================= LOGIN =================
@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            "message": "All fields are required"
        }), 400

    # FIND USER
    cursor.execute(
        "SELECT * FROM users WHERE username=%s",
        (username,)
    )

    user = cursor.fetchone()

    if not user:
        return jsonify({
            "message": "Invalid username or password"
        }), 401

    # CHECK PASSWORD
    if bcrypt.check_password_hash(user['password'], password):

        session['user'] = {
            "id": user['id'],
            "username": user['username'],
            "email": user['email'],
            "role": user['role'],
            "created_at": str(user['created_at'])
        }

        return jsonify({
            "message": "Login successful",
            "username": user['username'],
            "role": user['role']
        }), 200

    return jsonify({
        "message": "Invalid username or password"
    }), 401


# ================= DASHBOARD =================
@app.route('/dashboard', methods=['GET'])
def dashboard():

    if 'user' not in session:
        return jsonify({
            "message": "Unauthorized"
        }), 401

    return jsonify({
        "message": "Welcome",
        "user": session['user']
    }), 200


# ================= PROFILE =================
@app.route('/profile', methods=['GET'])
def profile():

    if 'user' not in session:
        return jsonify({
            "message": "Unauthorized"
        }), 401

    return jsonify(session['user']), 200


# ================= LOGOUT =================
@app.route('/logout', methods=['GET'])
def logout():

    session.pop('user', None)

    return jsonify({
        "message": "Logged out successfully"
    }), 200


# ================= MAIN =================
if __name__ == '__main__':
    app.run(debug=True)