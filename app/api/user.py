from app.api import bp

@bp.route('/users', methods=['GET'])
def get_users():
    return {'msg': 'Hello, World!'}