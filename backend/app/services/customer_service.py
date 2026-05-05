from app.extensions import db, get_redis_client
from app.models.customer import Customer
from app.utils.pagination import paginate
from datetime import datetime, timedelta
import re

class CustomerService:
    """客户服务"""
    
    @staticmethod
    def create_customer(data, source='小程序'):
        phone = data.get('phone', '')
        if not CustomerService._validate_phone(phone):
            return None, '手机号码格式不正确'
        
        if source != '后台添加' and CustomerService._check_rate_limit(phone):
            return None, '提交过于频繁，请稍后再试'
        
        customer = Customer(
            name=data['name'],
            phone=phone,
            wechat=data.get('wechat'),
            province=data.get('province'),
            city=data.get('city'),
            building_area_budget=data.get('building_area_budget'),
            product_id=data.get('product_id'),
            product_title=data.get('product_title'),
            source=source
        )
        db.session.add(customer)
        db.session.commit()
        
        if source != '后台添加':
            CustomerService._set_rate_limit(phone)
        return customer.to_dict(), None
    
    @staticmethod
    def _validate_phone(phone):
        """验证手机号码格式"""
        pattern = r'^1[3-9]\d{9}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def _check_rate_limit(phone):
        """检查提交频率限制"""
        redis_client = get_redis_client()
        if redis_client is None:
            return False
        key = f'customer_rate_limit:{phone}'
        count = redis_client.get(key)
        return count is not None and int(count) > 0
    
    @staticmethod
    def _set_rate_limit(phone):
        """设置提交频率限制（1分钟）"""
        redis_client = get_redis_client()
        if redis_client is None:
            return
        key = f'customer_rate_limit:{phone}'
        redis_client.setex(key, 60, 1)
    
    @staticmethod
    def get_customer_list(keyword=None, status=None, start_date=None, end_date=None, page=1, per_page=10):
        query = Customer.query
        
        if keyword:
            query = query.filter(
                (Customer.name.like(f'%{keyword}%')) |
                (Customer.phone.like(f'%{keyword}%')) |
                (Customer.wechat.like(f'%{keyword}%'))
            )
        
        if status:
            query = query.filter(Customer.status == status)
        
        if start_date:
            query = query.filter(Customer.created_at >= start_date)
        
        if end_date:
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Customer.created_at < end_datetime)
        
        query = query.order_by(Customer.created_at.desc())
        items, total, page, per_page = paginate(query, page, per_page)
        
        return [item.to_dict() for item in items], total, page, per_page
    
    @staticmethod
    def get_customer_detail(customer_id):
        customer = Customer.query.get(customer_id)
        return customer.to_dict() if customer else None
    
    @staticmethod
    def update_customer_status(customer_id, status):
        customer = Customer.query.get(customer_id)
        if not customer:
            return None
        customer.status = status
        db.session.commit()
        return customer.to_dict()
    
    @staticmethod
    def update_customer_remark(customer_id, remark):
        customer = Customer.query.get(customer_id)
        if not customer:
            return None
        customer.remark = remark
        db.session.commit()
        return customer.to_dict()
    
    @staticmethod
    def get_statistics():
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())
        
        week_ago = today - timedelta(days=7)
        week_start = datetime.combine(week_ago, datetime.min.time())
        
        month_ago = today - timedelta(days=30)
        month_start = datetime.combine(month_ago, datetime.min.time())
        
        today_count = Customer.query.filter(Customer.created_at.between(today_start, today_end)).count()
        week_count = Customer.query.filter(Customer.created_at >= week_start).count()
        month_count = Customer.query.filter(Customer.created_at >= month_start).count()
        total_count = Customer.query.count()
        
        return {
            'today': today_count,
            'week': week_count,
            'month': month_count,
            'total': total_count
        }