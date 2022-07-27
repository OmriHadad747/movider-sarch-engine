import os
from flask import Flask
from app import config


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config.DevConfig)

    with app.app_context():
        from app import extenstions
        extenstions.scheduler.init_app(app)
    
        from app.routes import search_engine
        app.register_blueprint(search_engine.search_engine_bp)

        from app.utils import scheduled_tasks
        
       # preventing from starting the scheduler twice (Werkzug launches two threads in order to reload the flask application on changes made)
        if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
            extenstions.scheduler.start()

        return app