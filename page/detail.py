from flask import Blueprint, render_template, abort
from models import HouseInfo, db

detail_page = Blueprint('detail_page', __name__)


@detail_page.route('/house/<int:house_id>')
def house_detail(house_id):
    """渲染房屋详情页 (Render house detail page)"""
    house = HouseInfo.query.get_or_404(house_id)

    if house.page_views is None:
        house.page_views = 0
    house.page_views += 1
    db.session.commit()

    return render_template('detail.html', house=house)
