def success(data=None, message='success'):
    return {
        'code': 200,
        'message': message,
        'data': data
    }

def error(code, message):
    return {
        'code': code,
        'message': message,
        'data': None
    }

def paginated(items, page, per_page, total):
    pages = (total + per_page - 1) // per_page
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': pages
    }