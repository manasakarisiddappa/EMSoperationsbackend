from flask import Flask
from flask_cors import CORS  
from config.config import Config
from config.database import init_db
from routes.employee_routes import routes_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)
    app.register_blueprint(routes_bp)
    CORS(app)  

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
