import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flames_login'

mysql = MySQL(app)

# Debugging: Test MySQL Connection
with app.app_context():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        print("✅ MySQL connection successful!")
        cur.close()
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")

# Ensure users table exists
with app.app_context():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)
        mysql.connection.commit()
        cur.close()
        print("✅ Users table checked/created successfully.")
    except Exception as e:
        print(f"❌ Error creating users table: {e}")

# Routes
@app.route('/')
def home():
    if 'logged_in' in session:
          return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = sha256_crypt.hash(password)

        # Debugging: Print received data
        print(f"Received Registration: Username={username}, Password={password}")

        try:
            with mysql.connection.cursor() as cur:
                cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
                mysql.connection.commit()
                flash('✅ Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
        except Exception as e:
            logging.error(f"❌ Error during registration: {e}")
            flash('❌ Registration failed. Username might already exist.', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        # Debugging: Print received login data
        print(f"Login Attempt: Username={username}")

        try:
            with mysql.connection.cursor() as cur:
                result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
                if result > 0:
                    data = cur.fetchone()
                    stored_password = data[2]  # Password is in the 3rd column (0-based index)

                    # Verify password
                    if sha256_crypt.verify(password_candidate, stored_password):
                        session['logged_in'] = True
                        session['username'] = username
                        flash('✅ Login successful!', 'success')
                        return redirect(url_for('home'))
                    else:
                        flash('❌ Incorrect password!', 'danger')
                else:
                    flash('❌ Username not found!', 'danger')
        except Exception as e:
            logging.error(f"❌ Error during login: {e}")
            flash('❌ Login failed. Please try again.', 'danger')

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.clear()
    flash('✅ You have been logged out.', 'success')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)

