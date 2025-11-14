# 现代化内容管理系统

这是一个现代化的Python网站项目，实现了以下功能：
1. 用户登录系统
2. 登录后可添加文本内容并保存
3. 在页面上以表格形式展示所有保存的内容及其时间

## 功能说明

- 默认用户名：`admin`
- 默认密码：`778899`
- 登录后可以添加新的文本内容
- 所有内容会连同保存时间一起显示在表格中

## 方案一：使用Flask（传统Web应用）

### 运行环境

- Python 3.x
- Flask
- Bootstrap 5

### 安装与运行

1. 克隆或下载本项目到本地

2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

3. 运行应用：
   ```
   python app.py
   ```

4. 在浏览器中访问 `http://127.0.0.1:5000`

## 方案二：使用Streamlit（现代化数据应用）

### 运行环境

- Python 3.x
- Streamlit
- Pandas

### 安装与运行

1. 克隆或下载本项目到本地

2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

3. 运行应用：
   ```
   streamlit run streamlit_app.py
   ```

4. 应用将在浏览器中自动打开

## GitHub部署指南

### 使用Streamlit Community Cloud部署（推荐）

1. 将此代码推送到您的GitHub仓库（您的GitHub账户名：maxzackye）
2. 访问 [Streamlit Community Cloud](https://streamlit.io/cloud)
3. 点击"New app"并连接您的GitHub仓库
4. 选择正确的分支和文件（streamlit_app.py）
5. 点击"Deploy!"完成部署

详细部署说明请参见 [DEPLOYMENT.md](file:///g%3A/py/%E6%96%87%E4%BB%B6/DEPLOYMENT.md) 文件。

### 使用GitHub Actions部署

本项目已包含GitHub Actions配置文件（.github/workflows/deploy.yml），可根据需要进行定制。

## 现代化设计特点

### Streamlit版本
- 渐变背景设计
- 半透明卡片式布局
- 响应式用户界面
- 现代化配色方案

### Flask版本
- 渐变背景设计
- Bootstrap 5样式框架
- 卡片式内容展示
- 响应式布局

## 云部署重要注意事项

⚠️ **重要提醒**：在Streamlit Community Cloud等云平台上部署时，请注意以下几点：

1. **文件系统限制**：云平台上的文件系统通常是临时的，这意味着每次应用重启后[data.db](file:///g%3A/py/%E6%96%87%E4%BB%B6/data.db)数据库文件可能会被清除。对于生产环境，建议使用外部数据库服务。

2. **环境变量**：可以通过设置`DATABASE_PATH`环境变量来指定数据库文件的位置。

3. **依赖管理**：确保所有依赖都在`requirements.txt`文件中正确声明。

## 注意事项

如果在安装依赖时遇到"No space left on device"错误，请清理磁盘空间后重试。Streamlit和相关依赖需要足够的空间来安装。

## 数据存储

项目使用SQLite数据库存储用户信息和内容数据，数据库文件会自动创建为 `data.db`。

## 目录结构

```
.
├── app.py              # Flask主应用程序文件
├── streamlit_app.py    # Streamlit主应用程序文件
├── requirements.txt    # 依赖包列表
├── Procfile            # 部署配置文件
├── README.md           # 项目说明文档
├── DEPLOYMENT.md       # 详细部署指南
├── templates/          # Flask HTML模板目录
│   ├── base.html       # 基础模板
│   ├── index.html      # 主页模板
│   └── login.html      # 登录页模板
├── .github/workflows/  # GitHub Actions工作流目录
│   └── deploy.yml      # 部署配置文件
└── data.db             # SQLite数据库文件（运行后自动生成）
```