from flask import Blueprint, request, jsonify, session
from models import db, UserInfo
from werkzeug.security import generate_password_hash, check_password_hash
import re

user_api = Blueprint('user_api', __name__)


# --- 注册、登录、退出函数保持不变 ---
@user_api.route('/register', methods=['POST'])
def register():
    # ... (code from previous step)
    pass


@user_api.route('/login', methods=['POST'])
def login():
    # ... (code from previous step)
    pass


@user_api.route('/logout')
def logout():
    # ... (code from previous step)
    pass


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
