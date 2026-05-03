from flask import current_app


def fix_image_url(image_url):
    if not image_url:
        return image_url

    if image_url.startswith('http://localhost') or image_url.startswith('http://127.0.0.1'):
        filename = image_url.rsplit('/')[-1] if '/' in image_url else image_url
        base = current_app.config['LOCAL_BASE_URL'].rstrip('/')
        return base + '/' + filename

    if image_url.startswith('http'):
        return image_url

    base = current_app.config['LOCAL_BASE_URL']
    if image_url.startswith('/uploads/'):
        return base.replace('/uploads', '') + image_url
    return base + '/' + image_url
