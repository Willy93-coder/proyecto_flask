from flask import flash, redirect, render_template, request, url_for
from flask import Blueprint
from flask_login import login_required, login_user, logout_user, current_user

from forms import CreateBlog, LoginForm, RegisterForm
from models import User, Blog, db
from werkzeug.security import generate_password_hash, check_password_hash


main = Blueprint('main', __name__)

@main.route("/")
def home():
   return render_template("index.html")

@main.route("/adios")
def bye():
   return "<p>Adios!</p>"

# Ruta login
@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Obtener los datos del formulario
        username = request.form.get("username")
        password = request.form.get("password")
        # Buscar el usuario en la base de datos
        user = User.query.filter_by(username = username).first()
        # Comprobar que existe y que la contraseña coincide
        if user and check_password_hash(user.password, password):
            # Si existe, iniciar sesion
            login_user(user)
            return redirect(url_for("main.private"))
        else:
            # Si no, error
            flash("Error en el login")
    return render_template("login.html", form = form)

# Ruta registro
@main.route("/registro", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Obtener los datos del formulario
        username = request.form.get("username")
        password = request.form.get("password")
        # Comprobar si el usuario existe
        user_exists = User.query.filter_by(username=username).first()
        # Si existe, error y redireccionamos
        if user_exists:
            flash("Usuario ya existe")
            return redirect(url_for("main.login"))
        # Si no existe, lo creamos
        new_user = User(username = username, password = generate_password_hash(password))
        #añadimos el usuario a la base de datos
        db.session.add(new_user)
        db.session.commit()
        # Y redirijimos al login
        flash("Usuario registrado con éxito")
        return redirect(url_for("main.login"))
    return render_template("register.html", form = form)

# Ruta privada
@main.route("/privada")
@login_required
def private():
    return render_template("private.html")

# Ruta creacion blog
@main.route("/creacion-blog", methods=["GET", "POST"])
@login_required
def createBlog():
    # Obtener los datos del formulario
    title = request.form.get("title")
    content = request.form.get("content")
    form = CreateBlog()
    if form.validate_on_submit():
        blog = Blog(title = title, content = content, user = current_user.id)
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for("main.posts"))
    else:
        flash("La entrada del blog no se ha hecho")
    return render_template("blog.html", form = form)

# Ruta posts
@main.route("/posts")
def posts():
   posts = Blog.query.all()
   return render_template("posts.html", posts = posts)

# Ruta de log out
@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))