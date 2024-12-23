from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# إنشاء اتصال بقاعدة البيانات
def get_db_connection():
    conn = sqlite3.connect('questions.db')
    conn.row_factory = sqlite3.Row
    return conn

# صفحة إدخال الأسئلة والأجوبة
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO questions (question, answer) VALUES (?, ?)', (question, answer))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('index.html')

# صفحة البحث عن الأسئلة
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        algorithm = request.form['algorithm']
        
        conn = get_db_connection()
        if algorithm == "Boolean":
            results = conn.execute('SELECT * FROM questions WHERE question LIKE ?', ('%' + query + '%',)).fetchall()
        elif algorithm == "Extended Boolean":
            results = conn.execute('SELECT * FROM questions WHERE question LIKE ?', ('%' + query + '%',)).fetchall()
        elif algorithm == "Vector Space":
            results = conn.execute('SELECT * FROM questions WHERE question LIKE ?', ('%' + query + '%',)).fetchall()
        
        conn.close()
        
    return render_template('search.html', results=results)

# إعداد قاعدة البيانات
def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT NOT NULL, answer TEXT NOT NULL)')
    conn.close()

if __name__ == '__main__':
    init_db()  # إعداد قاعدة البيانات عند بدء التطبيق
    app.run(debug=True)