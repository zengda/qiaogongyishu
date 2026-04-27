from flask import Blueprint, request
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app.models.admin import Admin
from app.utils.response import success, error

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/wx-login', methods=['POST'])
def wx_login():
    """微信登录（模拟实现）"""
    data = request.get_json()
    code = data.get('code')
    
    if not code:
        return error(400, '缺少code参数'), 400
    
    openid = f'wx_{code[-10:]}'
    token = jwt.encode({
        'openid': openid,
        'exp': datetime.now() + timedelta(days=7)
    }, 'wx-secret-key', algorithm='HS256')
    
    return success({
        'token': token,
        'openid': openid
    })

@auth_bp.route('/admin/auth/login', methods=['POST'])
def admin_login():
    """管理员登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return error(400, '用户名或密码不能为空'), 400
    
    admin = Admin.query.filter_by(username=username).first()
    if not admin or not admin.is_active:
        return error(401, '用户名或密码错误'), 401
    
    if not admin.check_password(password):
        return error(401, '用户名或密码错误'), 401
    
    admin.last_login_at = datetime.now()
    from app.extensions import db
    db.session.commit()
    
    token = jwt.encode({
        'user_id': admin.id,
        'username': admin.username,
        'role': admin.role,
        'exp': datetime.now() + timedelta(hours=24)
    }, 'your-jwt-secret-key-here', algorithm='HS256')
    
    return success({
        'token': token,
        'user': admin.to_dict()
    })

@auth_bp.route('/admin/auth/logout', methods=['POST'])
def admin_logout():
    """管理员登出"""
    return success(message='登出成功')

@auth_bp.route('/admin/auth/password', methods=['PUT'])
def change_password():
    """修改密码"""
    from app.utils.decorators import admin_required
    from flask import g
    
    @admin_required
    def do_change():
        data = request.get_json()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return error(400, '请提供旧密码和新密码'), 400
        
        admin = g.current_admin
        if not admin.check_password(old_password):
            return error(400, '旧密码不正确'), 400
        
        admin.password_hash = generate_password_hash(new_password)
        from app.extensions import db
        db.session.commit()
        
        return success(message='密码修改成功')
    
    return do_change()