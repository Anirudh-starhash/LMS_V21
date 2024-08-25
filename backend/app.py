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
from flask_caching import Cache
from application.tasks import celery_test,celery_beat,monthly_report
from celery.result import AsyncResult
from celery import Celery

app=None
celery=None





def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app():
    global celery, mail

    app = Flask(__name__)
  

    # Import blueprints here to avoid circular imports
   

    app.register_blueprint(user_blueprint, url_prefix='/api')
    app.register_blueprint(lib_blueprint, url_prefix='/api')
    app.register_blueprint(sec_blueprint, url_prefix='/api')
    app.register_blueprint(book_blueprint, url_prefix='/api')

    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is set up")
    else:
        print('Starting local Development')
        app.config.from_object(LocalDevelopmentConfig)
        app.config['SECRET_KEY'] = "Secret is meant to be Secret"
        app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
        db.init_app(app)
        app.app_context().push()
        app.config.update(
            CELERY_BROKER_URL='redis://localhost:6379/0',
            CELERY_RESULT_BACKEND='redis://localhost:6379/0'
        )
        app.config['CACHE_TYPE'] = 'RedisCache'
        app.config['CACHE_REDIS_HOST'] = 'localhost'
        app.config['CACHE_REDIS_PORT'] = 6379
        app.config['CACHE_REDIS_DB'] = 0
        app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
        
        celery=make_celery(app)
        celery.set_default()

        # Initialize Celery and Mail after app config is updated

        return app,celery
    
app,celery=create_app()
CORS(app)
migrate=Migrate(app)
jwt=JWTManager(app)
celery = make_celery(app)
cache=Cache(app)



@app.route("/cache")
@cache.cached(timeout=30)
def index():
    return str(datetime.now())






    

    
with app.app_context():
    db.create_all()
    





if __name__=="__main__":
    app.run(debug=True)
    
