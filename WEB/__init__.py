from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # blueprint
    from WEB.views import main_views, time_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(time_views.bp)
    
    return app