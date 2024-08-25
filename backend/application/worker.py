from celery import Celery,Task
from flask import current_app as app

celery=Celery("Application Jobs")

class ContextTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

celery.Task = ContextTask