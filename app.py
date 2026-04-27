from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'hedgehog_secret_key'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Создаем папку для гифок, если её нет
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

users = {} 

@app.route('/')
def index():
    # Собираем список всех файлов из папки uploads
    gifs = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', gifs=gifs, user=session.get('user'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    if username and password:
        users[username] = password
        session['user'] = username
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'gif_file' not in request.files:
        return redirect(request.url)
    file = request.files['gif_file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
