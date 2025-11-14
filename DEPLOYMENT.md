# GitHub + Streamlit Community Cloud 部署指南

本文档详细介绍了如何将此项目通过GitHub部署到Streamlit Community Cloud。

## 部署前准备

1. 确保您有一个GitHub账户（您的账户名：maxzackye）
2. Fork本项目或将其推送至您的GitHub仓库

## 部署步骤

### 第一步：推送代码到GitHub

如果您还没有将代码推送到GitHub，请按以下步骤操作：

```bash
# 如果您是从本地初始化仓库
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/maxzackye/your-repo-name.git
git push -u origin main

# 如果您已经有一个远程仓库
git add .
git commit -m "Update for deployment"
git push origin main
```

### 第二步：部署到Streamlit Community Cloud

1. 访问 [Streamlit Community Cloud](https://share.streamlit.io/)
2. 使用您的GitHub账户登录
3. 点击"New app"按钮
4. 如果是第一次使用，需要授权Streamlit访问您的GitHub账户
5. 选择您刚刚推送的仓库
6. 在"Main file path"字段中，输入 `streamlit_app.py`
7. 保持其他设置为默认值
8. 点击"Deploy!"按钮

### 第三步：等待部署完成

部署过程通常需要几分钟时间。您可以在部署过程中看到实时日志。

## 配置说明

本项目已经包含了必要的部署配置文件：

- `Procfile`: 定义了应用启动命令
- `.github/workflows/deploy.yml`: GitHub Actions工作流配置
- `requirements.txt`: 项目依赖列表

## 自定义域名（可选）

如果您想为应用设置自定义域名：

1. 在Streamlit Community Cloud控制台中找到您的应用
2. 点击"Settings"选项卡
3. 在"Custom subdomain"字段中输入您想要的子域名
4. 点击"Save"保存设置

## 更新应用

当您需要更新应用时：

1. 将更改推送到GitHub仓库的main分支
2. 在Streamlit Community Cloud控制台中，进入您的应用
3. 点击"Reboot app"或者等待自动重新部署

## 故障排除

### 依赖问题

如果部署失败，请检查`requirements.txt`文件中的依赖项是否正确。

### 端口问题

Streamlit Community Cloud会自动分配端口，应用中使用`$PORT`环境变量获取端口号。

### 数据库问题

由于Streamlit Community Cloud的文件系统是临时的，每次重启后[data.db](file:///g%3A/py/%E6%96%87%E4%BB%B6/data.db)文件可能会丢失。在生产环境中建议使用外部数据库服务。

## 最佳实践

1. 保持`requirements.txt`文件更新
2. 定期提交代码到GitHub
3. 使用有意义的提交消息
4. 在本地测试后再部署到云端
5. 监控应用性能和错误日志

## 支持

如果您在部署过程中遇到任何问题，请参考以下资源：

- [Streamlit官方文档](https://docs.streamlit.io/)
- [Streamlit Community论坛](https://discuss.streamlit.io/)