from flask import Blueprint, render_template
from models import HouseInfo

index_page = Blueprint('index_page', __name__)


@index_page.route('/')
def index():
    """
    渲染首页。
    加载最新的6条房源和最热门的3条房源。
    """
    # --- 查询最新的6条房源 (按 publish_time 降序) ---
    # --- Query for the 6 newest houses (order by publish_time descending) ---
    newest_houses = HouseInfo.query.order_by(HouseInfo.publish_time.desc()).limit(6).all()

    # --- 查询浏览量最高的3条房源 (按 page_views 降序) ---
    # --- Query for the 3 most popular houses (order by page_views descending) ---
    popular_houses = HouseInfo.query.order_by(HouseInfo.page_views.desc()).limit(3).all()

    # --- 将两组数据都传递给模板 ---
    # --- Pass both datasets to the template ---
    return render_template(
        'index.html',
        newest_houses=newest_houses,
        popular_houses=popular_houses
    )

