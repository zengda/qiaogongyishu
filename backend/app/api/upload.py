from flask import Blueprint, request
from app.services.upload_service import UploadService
from app.utils.response import success, error
from app.utils.decorators import admin_required

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/admin/upload/image', methods=['POST'])
@admin_required
def upload_image():
    """上传图片"""
    if 'file' not in request.files:
        return error(400, '未提供文件'), 400
    
    file = request.files['file']
    if file.filename == '':
        return error(400, '文件名不能为空'), 400
    
    url, err = UploadService.upload_image(file)
    if err:
        return error(400, err), 400
    
    return success({'url': url})