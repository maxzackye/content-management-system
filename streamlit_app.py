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
    
    /* 添加内容按钮样式 */
    .add-content-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 999;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .add-content-btn:hover {
        opacity: 0.9;
        transform: scale(1.05);
    }
    
    /* 添加内容模态框样式 */
    .modal {
        display: none;
        position: fixed;
        z-index: 1000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.5);
    }
    
    .modal-content {
        background-color: white;
        margin: 10% auto;
        padding: 30px;
        border-radius: 10px;
        width: 80%;
        max-width: 600px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .close {
        color: #aaa;
        float: right;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
    }
    
    .close:hover {
        color: black;
    }
    
    .modal-header {
        border-bottom: 1px solid #eee;
        padding-bottom: 15px;
        margin-bottom: 20px;
    }
    
    .modal-body textarea {
        width: 100%;
        min-height: 150px;
        padding: 12px;
        border: 1px solid #ddd;
        border-radius: 5px;
        resize: vertical;
        font-family: inherit;
    }
    
    .modal-footer {
        margin-top: 20px;
        text-align: right;
    }
    
    .btn-save {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        cursor: pointer;
    }
    
    .btn-save:hover {
        opacity: 0.9;
    }
    
    .btn-cancel {
        background: #f1f1f1;
        color: #333;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        cursor: pointer;
        margin-right: 10px;
    }
    
    .btn-cancel:hover {
        background: #ddd;
    }
    
    /* 显示模态框的类 */
    .modal.show {
        display: block;
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
    if 'show_add_content_modal' not in st.session_state:
        st.session_state.show_add_content_modal = False
        
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
    
    # 使用Streamlit按钮替代纯HTML按钮，以确保交互功能
    if st.button("➕", key="add_content_fab", help="添加新内容"):
        st.session_state.show_add_content_modal = True
    
    # 添加内容的模态框
    if st.session_state.show_add_content_modal:
        with st.form("add_content_form"):
            st.subheader("➕ 添加新内容")
            content = st.text_area("请输入内容:", height=150, key="content_input")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                submit_button = st.form_submit_button("保存内容")
            with col2:
                cancel_button = st.form_submit_button("取消")
            
            if submit_button:
                if content.strip():
                    add_post(content)
                    st.session_state.show_add_content_modal = False
                    st.success("内容已成功保存!")
                    st.rerun()
                else:
                    st.warning("请输入内容后再保存")
            
            if cancel_button:
                st.session_state.show_add_content_modal = False
                st.rerun()

if __name__ == "__main__":
    # 添加错误处理
    try:
        main()
    except Exception as e:
        st.error(f"应用出现错误: {str(e)}")
        st.info("请刷新页面重试或联系管理员")