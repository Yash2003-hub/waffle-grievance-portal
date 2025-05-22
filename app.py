from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def init_db():
    with sqlite3.connect('grievance.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS grievances (
                id INTEGER PRIMARY KEY,
                title TEXT,
                message TEXT,
                mood TEXT
            )
        ''')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    session['user'] = username

    if username == 'waffle' and password == 'sweetie123':
        return redirect('/submit')
    elif username == 'smolu' and password == 'listenmodeON':
        return redirect('/dashboard')
    else:
        return "Invalid credentials", 401

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if 'user' not in session or session['user'] != 'waffle':
        return redirect('/')

    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        mood = request.form['mood']

        with sqlite3.connect('grievance.db') as conn:
            conn.execute('INSERT INTO grievances (title, message, mood) VALUES (?, ?, ?)', 
                         (title, message, mood))
        return render_template('thank_you.html', user='waffle')
    return render_template('submit.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session or session['user'] != 'smolu':
        return redirect('/')
    with sqlite3.connect('grievance.db') as conn:
        grievances = conn.execute('SELECT title, message, mood FROM grievances').fetchall()
    return render_template('admin.html', grievances=grievances)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)