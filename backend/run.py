import os
from flask_cors import CORS
from app import create_app
from app.extensions import db
from app.models import init_data

app = create_app(os.getenv('FLASK_ENV', 'default'))

allowed_origins = [
    'http://localhost:3000',
    'http://localhost:5001',
    'https://qgys.rongyun.online',
    'http://qgys.rongyun.online',
]
CORS(app, resources={r"/api/*": {"origins": allowed_origins}})

@app.cli.command('init-db')
def init_db():
    """初始化数据库"""
    with app.app_context():
        db.create_all()
        init_data()
        print('数据库初始化完成')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)