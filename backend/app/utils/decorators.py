from functools import wraps
import jwt
from flask import request, current_app, g
from app.models.admin import Admin

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return {'code': 401, 'message': '未提供认证Token', 'data': None}, 401
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            admin = Admin.query.get(payload['user_id'])
            if not admin or not admin.is_active:
                return {'code': 401, 'message': '管理员不存在或已禁用', 'data': None}, 401
            g.current_admin = admin
        except jwt.ExpiredSignatureError:
            return {'code': 401, 'message': 'Token已过期，请重新登录', 'data': None}, 401
        except jwt.InvalidTokenError:
            return {'code': 401, 'message': '无效的Token', 'data': None}, 401
        return f(*args, **kwargs)
    return decorated