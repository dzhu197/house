from flask import Flask
from models import db
import datetime

# 导入页面蓝图
# Import page blueprints
from page.index import index_page
from page.detail import detail_page
from page.user import user_page
from page.list import list_page

# 导入API蓝图
# Import API blueprints
from api.user import user_api

# 初始化 Flask 应用
# Initialize Flask application
app = Flask(__name__)

# --- 数据库配置 (Database Configuration) ---
# !!! 重要: 请将 'your_password' 替换为您的 MySQL root 密码 !!!
# !!! IMPORTANT: Please replace 'your_password' with your MySQL root password !!!
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/house'

# 设置为 False 可以提高性能，除非你需要追踪对象的修改
# Setting to False improves performance, unless you need to track object modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 用于 session 加密的密钥，请务必修改为一个复杂的随机字符串
# Secret key for session encryption. Be sure to change this to a complex random string.
app.config['SECRET_KEY'] = 'a_very_secret_and_random_key_for_session'

# 将 db 对象与 Flask app 关联
# Associate the db object with the Flask app
db.init_app(app)

# --- 注册蓝图 (Register Blueprints) ---
app.register_blueprint(index_page, url_prefix='/')
app.register_blueprint(detail_page, url_prefix='/')
app.register_blueprint(user_page, url_prefix='/')
app.register_blueprint(list_page, url_prefix='/')
app.register_blueprint(user_api, url_prefix='/')

# --- 自定义模板过滤器 (Custom Template Filter) ---
@app.template_filter('timestamp_to_date')
def timestamp_to_date(timestamp):
    """将时间戳转换为 'YYYY-MM-DD' 格式的日期字符串"""
    """Converts a timestamp to a date string in 'YYYY-MM-DD' format."""
    if isinstance(timestamp, (int, float)):
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    return timestamp

# 当直接运行这个脚本时，启动Flask开发服务器
# If this script is executed directly, run the Flask development server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)

