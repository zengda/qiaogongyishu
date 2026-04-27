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