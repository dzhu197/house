# models.py

from flask_sqlalchemy import SQLAlchemy

# 这已经是解决循环导入问题的正确模式
# This is already the correct pattern to solve the circular import issue
db = SQLAlchemy()

class HouseInfo(db.Model):
    """对应数据库中的 house_info 表 (完全匹配)"""
    """Corresponds to the 'house_info' table (Fully matched)"""
    __tablename__ = 'house_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    rooms = db.Column(db.String(100))
    area = db.Column(db.String(100))
    price = db.Column(db.String(100))
    direction = db.Column(db.String(100))
    rent_type = db.Column(db.String(100))
    region = db.Column(db.String(100))
    block = db.Column(db.String(100))
    address = db.Column(db.String(200))
    traffic = db.Column(db.String(100))
    publish_time = db.Column(db.Integer)
    facilities = db.Column(db.Text)
    highlights = db.Column(db.Text)
    matching = db.Column(db.Text)
    travel = db.Column(db.Text)
    page_views = db.Column(db.Integer)
    landlord = db.Column(db.String(30))
    phone_num = db.Column(db.String(100))
    house_num = db.Column(db.String(100))

    def __repr__(self):
        return f'<HouseInfo {self.title}>'

class UserInfo(db.Model):
    """对应数据库中的 user_info 表 (已根据截图修正)"""
    """Corresponds to the 'user_info' table (Corrected based on screenshot)"""
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # 密码长度设置为255以存储加密哈希
    # Password length set to 255 to store encrypted hash
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # --- The following are corrections based on your screenshot ---
    addr = db.Column(db.String(100))
    collect_id = db.Column(db.String(250))
    seen_id = db.Column(db.String(250))
    # --- 修正结束 ---

    def __repr__(self):
        return f'<UserInfo {self.name}>'

class HouseRecommend(db.Model):
    """对应数据库中的 house_recommend 表 (完全匹配)"""
    """Corresponds to the 'house_recommend' table (Fully matched)"""
    __tablename__ = 'house_recommend'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    house_id = db.Column(db.Integer)
    title = db.Column(db.String(100))
    address = db.Column(db.String(100))
    block = db.Column(db.String(100))
    score = db.Column(db.Integer)

    def __repr__(self):
        return f'<HouseRecommend user_id={self.user_id} house_id={self.house_id}>'
