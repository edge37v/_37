from flask import g, abort, jsonify, request, url_for
from app import db
from app.models import User
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request

@bp.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'yep'})

@bp.route('/user_search/<query>')
@token_auth.login_required
def user_search(query):
    query = User.query.search(query).all()
    data = User.to_collection_dict(query, 'api.search')
    return jsonify(data)

from app.api.learning import lessons_sb, lessons_sb_yr, lessons_sb_yr_md, lessons_sb_yr_md_lv, \
    lesson, get_plans