from flask import Blueprint, request
from app.services.customer_service import CustomerService
from app.utils.response import success, error, paginated

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/customers', methods=['POST'])
def create_customer():
    """创建客户"""
    data = request.get_json()
    
    if not data.get('name') or not data.get('phone'):
        return error(400, '姓名和手机号为必填项'), 400
    
    customer, err = CustomerService.create_customer(data)
    if err:
        return error(400, err), 400
    
    return success(customer)

@customer_bp.route('/customers', methods=['GET'])
def get_customer_list():
    """获取客户列表"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    keyword = request.args.get('keyword')
    status = request.args.get('status')
    
    items, total, page, per_page = CustomerService.get_customer_list(
        keyword=keyword,
        status=status,
        page=page,
        per_page=per_page
    )
    
    return paginated(items, total, page, per_page)

@customer_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer_detail(customer_id):
    """获取客户详情"""
    customer = CustomerService.get_customer_detail(customer_id)
    if not customer:
        return error(404, '客户不存在'), 404
    
    return success(customer)

@customer_bp.route('/customers/<int:customer_id>/status', methods=['PATCH'])
def update_customer_status(customer_id):
    """更新客户状态"""
    data = request.get_json()
    status = data.get('status')
    
    if not status:
        return error(400, '状态不能为空'), 400
    
    customer = CustomerService.update_customer_status(customer_id, status)
    if not customer:
        return error(404, '客户不存在'), 404
    
    return success(customer)

@customer_bp.route('/customers/<int:customer_id>/remark', methods=['PATCH'])
def update_customer_remark(customer_id):
    """更新客户备注"""
    data = request.get_json()
    remark = data.get('remark')
    
    customer = CustomerService.update_customer_remark(customer_id, remark)
    if not customer:
        return error(404, '客户不存在'), 404
    
    return success(customer)

@customer_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """删除客户"""
    customer = CustomerService.get_customer_detail(customer_id)
    if not customer:
        return error(404, '客户不存在'), 404
    
    from app.extensions import db
    from app.models.customer import Customer
    customer_obj = Customer.query.get(customer_id)
    db.session.delete(customer_obj)
    db.session.commit()
    
    return success(None, '删除成功')

@customer_bp.route('/customers/export', methods=['GET'])
def export_customers():
    """导出客户列表"""
    from io import BytesIO
    from flask import send_file
    
    keyword = request.args.get('keyword')
    status = request.args.get('status')
    
    items, _, _, _ = CustomerService.get_customer_list(
        keyword=keyword,
        status=status,
        page=1,
        per_page=10000
    )
    
    output = BytesIO()
    try:
        import xlsxwriter
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('客户列表')
        
        headers = ['ID', '姓名', '手机号', '微信号', '省份', '城市', '建房面积预算', '意向产品', '状态', '创建时间']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)
        
        status_text_map = {
            'new': '新客户',
            'contacted': '已联系',
            'followed': '跟进中',
            'closed': '已成交'
        }
        
        for row, item in enumerate(items, start=1):
            worksheet.write(row, 0, item['id'])
            worksheet.write(row, 1, item['name'])
            worksheet.write(row, 2, item['phone'])
            worksheet.write(row, 3, item['wechat'] or '')
            worksheet.write(row, 4, item['province'] or '')
            worksheet.write(row, 5, item['city'] or '')
            worksheet.write(row, 6, item['building_area_budget'] or '')
            worksheet.write(row, 7, item['product_title'] or '')
            worksheet.write(row, 8, status_text_map.get(item['status'], item['status']))
            worksheet.write(row, 9, item['created_at'])
        
        workbook.close()
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            download_name='客户列表.xlsx',
            as_attachment=True
        )
    except ImportError:
        return error(500, '导出功能依赖 xlsxwriter 库'), 500
