import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configurar aplicação
app = Flask(__name__)

# Assegurar que os modelos sejam auto-recarregados
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Assegurar que as respostas não sejam armazenadas em cache
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Filtro personalizado
app.jinja_env.filters["usd"] = usd

# Configurar a sessão para usar o sistema de arquivos (ao invés de cookies assinados)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configurar a biblioteca do CS50 para usar o banco de dados SQLite
db = SQL("sqlite:///finance.db")

# Certifique-se de que a chave API esteja definida
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Esqueça qualquer user_id
    session.clear()

    # O usuário chegou à rota via POST (como ao enviar um formulário via POST)
    if request.method == "POST":

     # Assegurar que o nome de usuário foi submetido
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Assegurar que a senha foi enviada
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Consultar banco de dados para nome de usuário
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Certifique-se de que o nome de usuário existe e a senha está correta
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Lembrar qual usuário efetuou o login
        session["user_id"] = rows[0]["id"]

        # Redirecionar o usuário para a página inicial
        return redirect("/")

    # O usuário chegou à rota via GET (como clicando em um link ou via redirecionamento)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        senha =  request.form.get("senha")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Introduza o nome de usuário")
        if not senha:
            return apology("Introduza uma senha")
        if senha != senha:
            return apology("Must give confirmation")

        hash =  generate_password_hash(senha)

        try:
            # Inserindo os novos usuários e sua senha criptografada no banco de dado
            new = db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, hash)
        except:
            return apology("Usuário já existe")

        # Salvar o novo usuário
        session["user_id"] = new

        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
