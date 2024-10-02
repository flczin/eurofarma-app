import os
from flask import Flask, current_app, render_template, request, redirect, url_for, session, flash, send_from_directory, jsonify, abort
from pymongo import MongoClient
import dotenv
import ollama


app = Flask(__name__)
app.secret_key = dotenv.get_key(".env", "SECRET")

client = MongoClient(dotenv.get_key(".env", "MONGODB_URI"))
db = client.eurofarma
users_collection = db.users

ai_client = ollama.Client(host=dotenv.get_key(".env", "OLLAMA_URI"))

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
    

@app.route('/download_pdf/<path:filename>')
def download_pdf(filename):
    try:
        manuais = os.path.join(current_app.root_path, "manuais")
        return send_from_directory(manuais, filename, as_attachment=True, mimetype='application/pdf')
    except FileNotFoundError:
        abort(404)


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/ia', methods=['POST'])
def generate_response():
    data = request.get_json()
    text = data.get('text')

    try:
        response = ai_client.chat(model='gemma2:2b', messages=[
            {
                'role': 'user',
                'content': f'''Você possui vasto conhecimento sobre compliance, leis trabalhistas, responsabilidade social, sustentabilidade corporativa.
                Com isso responda a seguir: {text}. Responda o mais resumidamente possivel''',
            },
        ]) 

        if 'message' in response and 'content' in response['message']:
            return jsonify({'content': response['message']['content']}), 200
        else:
            return jsonify({"error": "Invalid response format"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host="0.0.0.0")
