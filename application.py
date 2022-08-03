import os
from flask import jsonify
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
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
    """Mostrar carteira de ações"""
    user_id = session["user_id"] 
    
    transactions_db = db.execute("SELECT symbol, SUM(shares) AS shares, prices FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    money_db = db.execute(" SELECT cash FROM users WHERE id = ?", user_id)
    money = money_db[0]["cash"] 
    
    
    return render_template("index.html", database = transactions_db, money = money ) 


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Compra de ações"""
    
    if request.method == "GET":
        return render_template("buy.html") 
    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        
        if not symbol:
            return apology("Deveria ter o simbolo")
        
        #consultar o preço atual de uma ação.
        estoque = lookup(symbol.upper())
        
        if estoque == None:
            return apology("Simbolo não existe") 
            
        if shares < 0:
            return apology("Ações não permitidas") 
            
        valor_da_transacao = shares * estoque["price"]
        
        user_id = session["user_id"] 
        user_money_db = db.execute("SELECT cash FROM users WHERE id= :id ", id = user_id)
        user_money = user_money_db[0]["cash"]
        
        # Checando se o user tem dinheiro na conta suficente para pagar 
        
        if user_money < valor_da_transacao:
            return apology("Você não tem dinheiro suficiente para comprar essa ação.")
        else:
            uptd_money = user_money - valor_da_transacao
            
            # Autalizar a quantidade do user
            db.execute(" UPDATE users SET cash = ? WHERE id = ?", uptd_money, user_id )
            
            data = datetime.datetime.now()
            
            db.execute("INSERT INTO transactions (user_id, symbol,shares, prices,data) VALUES (?,?,?,?,?)",user_id,estoque["symbol"], shares, estoque["price"], data )
            
            flash("Compra efetuada")
            
            return redirect("/")
            
        

@app.route("/history")
@login_required
def history():
    """Mostrar histórico de transações"""
    
    user_id = session["user_id"]
    transactions_db = db.execute("SELECT * FROM transactions WHERE user_id = :id", id = user_id)
    return render_template("history.html", transactions = transactions_db )

            
        

@app.route("/add_money", methods=["GET", "POST"])
@login_required
def add_money():
    """Adicionar dinheiro"""
    if request.method == "GET":
        return render_template("add.html")
    else:
        new_money = int(request.form.get("new_money"))
      
        if not new_money:
            return apology("Você deve fornecer dinheiro") 
        else:  
            user_id = session["user_id"]
            money_db = db.execute(" SELECT cash FROM users WHERE id = ?", user_id)
            money = money_db[0]["cash"] 
    
            uptd_money = new_money + money
                
                # Autalizar a quantidade do user
            db.execute(" UPDATE users SET cash = ? WHERE id = ?", uptd_money, user_id )
        
            flash("Transaçao bem sucedida.")
            
            return redirect("/") 
        
   
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Esqueça qualquer user_id
    session.clear()

    # O usuário chegou à rota via POST (como ao enviar um formulário via POST)
    if request.method == "POST":

     # Assegurar que o nome de usuário foi submetido
        if not request.form.get("username"):
            return apology("Introduza o nome de usuário.", 403)

        # Assegurar que a senha foi enviada
        elif not request.form.get("password"):
            return apology("Introduza a senha", 403)

        # Consultar banco de dados para nome de usuário
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Certifique-se de que o nome de usuário existe e a senha está correta
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("username ou senha inválida.", 403)

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
    """Obter cotação de estoque"""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        simbolo = request.form.get("simbolo")
        
        if not simbolo:
            return apology("Deveria ter o simbolo")
        
        estoque = lookup(simbolo.upper())
        
        if estoque == None:
            return apology("Simbolo não existe") 
            # enviando info fo back para o front 
        return render_template("quoted.html", name = estoque["name"] , price = estoque["price"], symbol = estoque["symbol"]) 
# ATENÇÃO: Para que a funçao lookup der certo, você tem que roda o programa em um console configurafo com a seguinte linha de comando: export API_KEY=pk_a5595b67022441f2863d3f6faba5642e
        
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
    """Vender ações"""
    
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_user = db.execute(" SELECT symbol FROM transactions WHERE user_id  = :id GROUP BY symbol HAVING SUM(shares) > 0 ", id = user_id)
        return render_template("sell.html", symbols = [row["symbol"] for row in symbols_user ])
    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        
        if not symbol:
            return apology("Deveria ter o simbolo")
        
        #consultar o preço atual de uma ação.
        estoque = lookup(symbol.upper())
        
        if estoque == None:
            return apology("Simbolo não existe") 
            
        if shares < 0:
            return apology("Ações não permitidas") 
        
        
        valor_da_transacao = shares * estoque["price"]
        
        user_id = session["user_id"] 
        user_money_db = db.execute("SELECT cash FROM users WHERE id= :id ", id = user_id)
        user_money = user_money_db[0]["cash"]
        
        # Assegurando que o user só venda o que tem 
        user_shares = db.execute("SELECT  SUM(shares) AS shares WHERE user_id=:id AND symbol = :symbol GROUP BY symbol",id = user_id, symbol = symbol)
        user_shares_real = user_shares[0]["shares"]
        
        if shares > user_shares_real:
            return apology("Você não tem essa quantidade ações para vender ")
        
        uptd_money = user_money + valor_da_transacao
            
            # Autalizar a quantidade do user
        db.execute(" UPDATE users SET cash = ? WHERE id = ?", uptd_money, user_id )
            
        data = datetime.datetime.now()
            
        db.execute("INSERT INTO transactions (user_id, symbol,shares, prices,data) VALUES (?,?,?,?,?)",user_id,estoque["symbol"], (-1)*shares, estoque["price"], data )
            
        flash("Vendido!")
            
        return redirect("/")
        
            
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
