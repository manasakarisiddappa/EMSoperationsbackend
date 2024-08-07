from config.config import db

def init_db(app):
    """
    Initializes the SQLAlchemy database with the provided Flask application.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()
