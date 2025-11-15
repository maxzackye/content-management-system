from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# 初始化数据库
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  content TEXT NOT NULL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # 添加默认用户（用户名: admin, 密码: 778899）
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  ('admin', '778899'))
    except sqlite3.IntegrityError:
        pass  # 用户已存在
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'username' in session:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('SELECT content, timestamp FROM posts ORDER BY timestamp DESC')
        posts = c.fetchall()
        conn.close()
        return render_template('index.html', posts=posts)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', 
                  (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add_post', methods=['POST'])
def add_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    content = request.form['content']
    if content:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('INSERT INTO posts (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    # 解决inotify实例限制问题
    # 在生产环境中禁用调试模式，或设置环境变量
    use_reloader = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=False, use_reloader=use_reloader)