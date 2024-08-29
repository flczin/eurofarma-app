from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import dotenv

app = Flask(__name__)
app.secret_key = dotenv.get_key(".env", "SECRET")

client = MongoClient(dotenv.get_key(".env", "MONGODB_URI"))
db = client.eurofarma
users_collection = db.users

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_collection.find_one({"username": username})
        
        if user and (password == user["password"]):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        flash('You must be logged in to access the dashboard', 'warning')
        return redirect(url_for('login'))


@app.route('/perguntas')
def perguntas():
    if 'username' in session:
        return render_template('perguntas.html', username=session['username'])
    else:
        flash('You must be logged in to access perguntas', 'warning')
        return redirect(url_for('login'))


@app.route('/manuais')
def manuais():
    if 'username' in session:
        return render_template('manuais.html', username=session['username'])
    else:
        flash('You must be logged in to access manuais', 'warning')
        return redirect(url_for('login'))


@app.route('/recursos')
def recursos():
    if 'username' in session:
        return render_template('recursos.html', username=session['username'])
    else:
        flash('You must be logged in to access recursos', 'warning')
        return redirect(url_for('login'))


@app.route('/relatorios')
def relatorios():
    if 'username' in session:
        return render_template('relatorios.html', username=session['username'])
    else:
        flash('You must be logged in to access relatorios', 'warning')
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
