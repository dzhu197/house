from flask import Blueprint, render_template, session, redirect, url_for
from models import UserInfo, HouseInfo

user_page = Blueprint('user_page', __name__)


@user_page.route('/user')
def user_profile():
    """
    渲染用户中心页，并加载用户的收藏和浏览历史。
    Render user profile page, and load user's collections and browsing history.
    """
    user_id = session.get('user_id')
    if not user_id:
        # 如果用户未登录，重定向到首页
        # If user is not logged in, redirect to homepage
        return redirect(url_for('index_page.index'))

    user = UserInfo.query.get(user_id)
    if not user:
        # 如果在数据库中找不到用户，清除 session 并重定向
        # If user not found in DB, clear session and redirect
        session.clear()
        return redirect(url_for('index_page.index'))

    # --- 处理收藏的房源 (Process collected houses) ---
    collected_houses = []
    if user.collect_id:
        # 分割ID字符串，转换为整数列表，并过滤掉可能的空字符串
        # Split the ID string, convert to integer list, and filter out possible empty strings
        collect_ids = [int(id_str) for id_str in user.collect_id.split(',') if id_str]
        if collect_ids:
            # 一次性查询所有收藏的房源
            # Query all collected houses at once
            collected_houses = HouseInfo.query.filter(HouseInfo.id.in_(collect_ids)).all()

    # --- 处理浏览过的房源 (Process seen houses) ---
    seen_houses = []
    if user.seen_id:
        seen_ids = [int(id_str) for id_str in user.seen_id.split(',') if id_str]
        if seen_ids:
            # 为了保持浏览顺序，可以创建一个ID到房源的映射
            # To preserve browsing order, a map from ID to house can be created
            seen_house_map = {house.id: house for house in HouseInfo.query.filter(HouseInfo.id.in_(seen_ids)).all()}
            seen_houses = [seen_house_map.get(id) for id in seen_ids if seen_house_map.get(id)]

    return render_template(
        'user.html',
        user=user,
        collected_houses=collected_houses,
        seen_houses=seen_houses
    )