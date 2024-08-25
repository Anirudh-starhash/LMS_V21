import os
from flask import Flask
from application.database import db
from application.config import LocalDevelopmentConfig
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from application.user_controllers import *
from application.book_controllers import *
from application.librarian_controllers import *
from application.section_controllers import *
from application.api import *
from flask_caching import Cache
from application.tasks import celery_test,celery_beat,monthly_report
from application import worker
from celery.result import AsyncResult
from celery import Celery
from flask_login import LoginManager
from flask_restful import Resource,Api

app=None
celery=None
api=None


def create_app():

    app = Flask(__name__)
    # Import blueprints here to avoid circular imports
    app.register_blueprint(user_blueprint, url_prefix='/api')
    app.register_blueprint(lib_blueprint, url_prefix='/api')
    app.register_blueprint(sec_blueprint, url_prefix='/api')
    app.register_blueprint(book_blueprint, url_prefix='/api')

    if os.getenv('ENV', "development") == "production":
        app.logger.warning("Currently no production config is set up")
        raise Exception("Currently no production config is set up")
    else:
        app.logger.info("Starting local development")
        print('Starting local Development')
        app.config.from_object(LocalDevelopmentConfig)
        db.init_app(app)
        app.app_context().push()
        app.config['SECRET_KEY'] = "Secret is meant to be Secret"
        app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
       
        api=Api(app)
        app.app_context().push()
        
        celery=worker.celery
        celery.conf.update(
            broker_url=app.config['CELERY_BROKER_URL'],
            result_backennd=app.config['CELERY_RESULT_BACKEND']
            
        )
        celery.Task=worker.ContextTask
        app.app_context().push()
        
        app.config['CACHE_TYPE'] = 'RedisCache'
        app.config['CACHE_REDIS_HOST'] = 'localhost'
        app.config['CACHE_REDIS_PORT'] = 6379
        app.config['CACHE_REDIS_DB'] = 0
        app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
        
        cache=Cache(app)
        cache.init_app(app)
        
        app.app_context().push()
        # Initialize Celery and Mail after app config is updated
        app.logger.info("App Setup Complete")

        return app,api,celery,cache
    
app,api,celery,cache=create_app()
CORS(app)
migrate=Migrate(app)
jwt=JWTManager(app)

@app.route("/cache")
@cache.cached(timeout=30)
def index():
    return str(datetime.now())

@app.errorhandler(404)
def page_not_found():
    return jsonify({
        'msg':'Page Not found'
    }),404
    
@app.errorhandler(401)
def not_authorized():
    return jsonify({
        'msg':'Not Authorized'
    }),401

with app.app_context():
    db.create_all()
    
if __name__=="__main__":
    app.run(debug=True)
    
