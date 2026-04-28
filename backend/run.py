import os
from app import create_app
from app.extensions import db
from app.models import init_data

app = create_app(os.getenv('FLASK_ENV', 'default'))

@app.cli.command('init-db')
def init_db():
    """初始化数据库"""
    with app.app_context():
        db.create_all()
        init_data()
        print('数据库初始化完成')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)