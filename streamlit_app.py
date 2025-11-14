import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import os

# 页面配置
st.set_page_config(
    page_title="内容管理系统",
    layout="wide"
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
    
    # 添加默认用户（用户名: admin, 密码: password）
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  ('admin', 'password'))
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
    st.title("📝 内容管理系统")
    
    # 初始化会话状态
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
        
    # 登录页面
    if not st.session_state.logged_in:
        st.subheader("用户登录")
        username = st.text_input("用户名", key="login_username")
        password = st.text_input("密码", type="password", key="login_password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("登录"):
                if authenticate(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"欢迎, {username}!")
                    st.experimental_rerun()
                else:
                    st.error("用户名或密码错误")
        with col2:
            if st.button("查看示例"):
                # 显示一些示例数据
                sample_data = pd.DataFrame({
                    '时间': ['2023-01-01 10:00:00', '2023-01-02 15:30:00'],
                    '内容': ['这是示例内容1', '这是示例内容2']
                })
                st.table(sample_data)
                
        st.info("默认账号: admin, 默认密码: password")
        return
    
    # 主页面
    st.sidebar.title(f"欢迎, {st.session_state.username}")
    if st.sidebar.button("退出登录"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.experimental_rerun()
    
    # 添加新内容
    st.subheader("添加新内容")
    content = st.text_area("请输入内容:", height=150, key="new_content")
    
    if st.button("保存"):
        if content.strip():
            add_post(content)
            st.success("内容已保存!")
            st.experimental_rerun()
        else:
            st.warning("请输入内容后再保存")
    
    # 显示历史内容
    st.subheader("历史内容")
    posts_df = get_posts()
    
    if not posts_df.empty:
        # 格式化列名
        posts_df.columns = ['内容', '时间']
        st.dataframe(posts_df, use_container_width=True)
    else:
        st.info("暂无内容，请添加新内容")

if __name__ == "__main__":
    main()