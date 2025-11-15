import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import os

# 页面配置
st.set_page_config(
    page_title="内容管理系统",
    layout="wide",
    page_icon="📝"
)

# 初始化数据库
def init_db():
    # 在云部署环境中使用绝对路径
    db_path = os.environ.get('DATABASE_PATH', 'data.db')
    conn = sqlite3.connect(db_path)
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

# 用户认证
def authenticate(username, password):
    db_path = os.environ.get('DATABASE_PATH', 'data.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', 
              (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# 添加内容
def add_post(content):
    db_path = os.environ.get('DATABASE_PATH', 'data.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO posts (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()

# 获取所有内容
def get_posts():
    db_path = os.environ.get('DATABASE_PATH', 'data.db')
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query('SELECT content, timestamp FROM posts ORDER BY timestamp DESC', conn)
    conn.close()
    return df

# 初始化数据库
init_db()

# 应用主体逻辑
def main():
    # 添加自定义CSS样式
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
    }
    .login-box {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        margin: 50px auto;
    }
    .content-box {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .header {
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    .logout-btn {
        float: right;
    }
    h1 {
        color: white;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    h2 {
        color: #333;
        border-bottom: 2px solid #667eea;
        padding-bottom: 10px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        opacity: 0.9;
    }
    .welcome-text {
        color: white;
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 页面标题
    st.markdown("<h1>📝 现代化内容管理系统</h1>", unsafe_allow_html=True)
    
    # 初始化会话状态
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
        
    # 登录页面
    if not st.session_state.logged_in:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.subheader("🔒 用户登录")
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        
        if st.button("登录"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"欢迎, {username}!")
                st.rerun()
            else:
                st.error("用户名或密码错误")
        
        st.info("默认账号密码均为: 778899")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # 主页面
    st.markdown(f'<div class="welcome-text">欢迎, <strong>{st.session_state.username}</strong>! 您已成功登录系统。</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("退出登录"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
    
    # 添加新内容
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.subheader("➕ 添加新内容")
    content = st.text_area("请输入内容:", height=150, key="new_content")
    
    if st.button("保存内容"):
        if content.strip():
            add_post(content)
            st.success("内容已成功保存!")
            st.rerun()
        else:
            st.warning("请输入内容后再保存")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 显示历史内容
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.subheader("📚 历史内容")
    posts_df = get_posts()
    
    if not posts_df.empty:
        # 格式化列名
        posts_df.columns = ['内容', '时间']
        st.dataframe(posts_df, use_container_width=True)
    else:
        st.info("暂无内容，请添加新内容")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    # 添加错误处理
    try:
        main()
    except Exception as e:
        st.error(f"应用出现错误: {str(e)}")
        st.info("请刷新页面重试或联系管理员")