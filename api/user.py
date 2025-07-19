from flask import Blueprint, request, jsonify, session
from models import db, UserInfo
from werkzeug.security import generate_password_hash, check_password_hash
import re

user_api = Blueprint('user_api', __name__)


@user_api.route('/register', methods=['POST'])
def register():
    """用户注册API接口 (User registration API endpoint)"""
    data = request.form
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not all([username, password, email]):
        return jsonify({'valid': 0, 'msg': '参数不完整 (Incomplete parameters)'})

    user = UserInfo.query.filter_by(name=username).first()
    if user:
        return jsonify({'valid': 0, 'msg': '该用户已被注册 (User already registered)'})

    email_user = UserInfo.query.filter_by(email=email).first()
    if email_user:
        return jsonify({'valid': 0, 'msg': '该邮箱已被注册 (Email already registered)'})

    hashed_password = generate_password_hash(password)

    new_user = UserInfo(name=username, password=hashed_password, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'valid': 1, 'msg': '注册成功 (Registration successful)'})


@user_api.route('/login', methods=['POST'])
def login():
    """用户登录API接口 (User login API endpoint)"""
    data = request.form
    username = data.get('username')
    password = data.get('password')

    user = UserInfo.query.filter_by(name=username).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['user_name'] = user.name
        return jsonify({'valid': 1, 'msg': '登录成功 (Login successful)'})

    return jsonify({'valid': 0, 'msg': '用户名或密码错误 (Incorrect username or password)'})


@user_api.route('/logout')
def logout():
    """用户退出登录API接口 (User logout API endpoint)"""
    session.clear()
    return jsonify({'valid': 1, 'msg': '退出成功 (Logout successful)'})


# +++ 新增: 用户信息更新接口 +++
# +++ ADDED: User info update endpoint +++
@user_api.route('/user/update', methods=['POST'])
def update_user_profile():
    """处理用户信息的表单提交"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'msg': '用户未登录，请先登录。'})

    user = UserInfo.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'msg': '用户不存在。'})

    data = request.form
    new_name = data.get('name')
    new_email = data.get('email')
    new_addr = data.get('addr')
    new_password = data.get('password')

    # --- 数据验证 ---
    if not all([new_name, new_email]):
        return jsonify({'success': False, 'msg': '昵称和邮箱不能为空。'})
    if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
        return jsonify({'success': False, 'msg': '请输入有效的邮箱地址。'})
    if UserInfo.query.filter(UserInfo.name == new_name, UserInfo.id != user_id).first():
        return jsonify({'success': False, 'msg': '该昵称已被使用。'})
    if UserInfo.query.filter(UserInfo.email == new_email, UserInfo.id != user_id).first():
        return jsonify({'success': False, 'msg': '该邮箱已被使用。'})

    # --- 更新数据 ---
    try:
        user.name = new_name
        user.email = new_email
        user.addr = new_addr

        # 如果用户输入了新密码，则更新密码
        if new_password:
            if len(new_password) < 6:
                return jsonify({'success': False, 'msg': '新密码长度不能少于6位'})
            user.password = generate_password_hash(new_password)

        db.session.commit()

        # 更新成功后，清除 session 让用户重新登录
        session.clear()

        return jsonify({'success': True, 'msg': '信息更新成功，请重新登录。'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'msg': f'更新失败: {str(e)}'})
