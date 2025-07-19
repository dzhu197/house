# app.py

import os
import datetime
from dotenv import load_dotenv
from flask import Flask, render_template

# 从我们新修改的 models.py 中导入 db 实例
# Import the db instance from our newly modified models.py
from models import db

# 您原有的蓝图导入保持不变
# Your original blueprint imports remain unchanged
from page.user import user_page
from page.list import list_page
from page.detail import detail_page
from page.index import index_page
from api.user import user_api

# 加载 .env 文件
# Load the .env file
load_dotenv()

app = Flask(__name__)

# --- 从环境变量加载配置 ---
# Load configuration from environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a_default_fallback_key_123')

# --- 使用 init_app 将 db 实例与 app 关联 ---
# Associate the db instance with the app using init_app
db.init_app(app)

# --- 您原有的蓝图注册保持不变 ---
# Your original blueprint registrations remain unchanged
app.register_blueprint(index_page, url_prefix='/')
app.register_blueprint(detail_page, url_prefix='/')
app.register_blueprint(user_page, url_prefix='/')
app.register_blueprint(list_page, url_prefix='/')
app.register_blueprint(user_api, url_prefix='/')

# --- 您原有的自定义模板过滤器保持不变 ---
# Your original custom template filter remains unchanged
@app.template_filter('timestamp_to_date')
def timestamp_to_date(timestamp):
    if isinstance(timestamp, (int, float)):
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    return timestamp

# 您原有的根路由保持不变
# Your original root route remains unchanged
@app.route('/')
def index():
    return render_template('index.html')

# 您原有的主程序入口保持不变
# Your original main entry point remains unchanged
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
