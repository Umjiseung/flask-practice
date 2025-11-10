from flask import Flask
from flask_restx import Api
from database import db
from resources import init_routes
from dotenv import load_dotenv
import logging
import os

app = Flask(__name__)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = (f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_DOCKER_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")

# mysql+pymysql://root:1234@mysql:3306/board

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
api = Api(app, version='1.0', title='Board API', description='게시판 CRUD API 예제')

init_routes(api)

logging.basicConfig(filename='/app/flask-error.log', level=logging.DEBUG)

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"DB 초기화 실패: {e}")
            logging.error(f"DB 초기화 실패: {e}")
            raise
    try:
        app.run(port=5001, debug=True)
    except Exception as e:
        app.logger.error(f"Flask 실행 실패: {e}")
        logging.error(f"Flask 실행 실패: {e}")
        raise
