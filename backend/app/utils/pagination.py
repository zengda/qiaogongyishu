def paginate(query, page, per_page):
    """分页查询辅助函数"""
    page = int(page) if page else 1
    per_page = int(per_page) if per_page else 10
    
    offset = (page - 1) * per_page
    items = query.offset(offset).limit(per_page).all()
    total = query.count()
    
    return items, total, page, per_page