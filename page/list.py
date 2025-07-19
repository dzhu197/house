from flask import Blueprint, render_template, request
from models import HouseInfo
from sqlalchemy import or_

list_page = Blueprint('list_page', __name__)


@list_page.route('/list')
def house_list():
    """渲染房屋列表页，支持按地区或户型搜索，并进行分页"""
    page = request.args.get('page', 1, type=int)

    # 获取搜索参数
    addr_query = request.args.get('addr', '')
    rooms_query = request.args.get('rooms', '')

    # 确定当前的搜索类型和值
    search_type = ''
    search_value = ''

    query = HouseInfo.query

    if addr_query:
        search_type = 'addr'
        search_value = addr_query
        search_term = f"%{addr_query}%"
        query = query.filter(or_(
            HouseInfo.title.ilike(search_term),
            HouseInfo.address.ilike(search_term),
            HouseInfo.region.ilike(search_term),
            HouseInfo.block.ilike(search_term)
        ))
    elif rooms_query:
        search_type = 'rooms'
        search_value = rooms_query
        search_term = f"%{rooms_query}%"
        query = query.filter(HouseInfo.rooms.ilike(search_term))

    # 按发布时间降序排序
    pagination = query.order_by(HouseInfo.publish_time.desc()).paginate(page=page, per_page=10, error_out=False)
    houses = pagination.items

    return render_template(
        'list.html',
        houses=houses,
        pagination=pagination,
        search_type=search_type,
        search_value=search_value
    )
