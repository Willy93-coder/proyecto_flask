from flask import Flask
from models import db, User
from routes import main
from flask_login import LoginManager

# Creamos la app
app = Flask(__name__)
# Creamos la configuracion del proyecto que se importa del archivo config.py
app.config.from_object('config.DevConfig')

# Configurar Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "main.login"

# Enseñamos a flask como cargar el usuario
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Inicializar la base de datos
db.init_app(app)

# Creamos las tablas
with app.app_context():
    db.create_all()

# Cargamos nuestras rutas
app.register_blueprint(main)