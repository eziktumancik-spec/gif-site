from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'dark_side_key' # Секретный ключ для сессий
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# "База данных" в памяти для примера (в реале лучше SQL)
users = {} # {логин: пароль}
gifs = []  # [{'owner': 'admin', 'filename': 'cat.gif'}]

@app.route('/')
def index():
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
def upload():
    if 'user' not in session:
        return "Сначала войди в систему, штурмовик!", 403
    
    file = request.files.get('gif')
    if file and file.filename.endswith('.gif'):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        gifs.append({'owner': session['user'], 'filename': filename})
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)