from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User
config_class = Config

app = Flask(__name__)
app.config.from_object(config_class)


# Initialize extensions here (if any)
# db.init_app(app)
# login_manager.init_app(app)

# Register blueprints here
from routes import main_bp
app.register_blueprint(main_bp)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User,int(user_id))



if __name__ == '__main__':
    with app.app_context():  # Push the application context
        db.create_all() 
    app.run(debug=True)

