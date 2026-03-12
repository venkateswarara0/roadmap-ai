from flask import Flask
from flask_login import LoginManager
from config import Config
from models.database import db
from routes.auth import auth_bp
from routes.roadmap import roadmap_bp
from routes.progress import progress_bp
from routes.quiz import quiz_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = Config.get_connection_string()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from models.user import User

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(roadmap_bp)
app.register_blueprint(progress_bp)
app.register_blueprint(quiz_bp)

if __name__ == '__main__':
    app.run(debug=True)