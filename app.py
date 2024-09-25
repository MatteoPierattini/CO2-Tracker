import datetime
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Templates fanno reload automatico
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configurazione sessione
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Sqlite database grazie alla libreria cs50
db = SQL("sqlite:///database.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    session.clear
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return "Devi inserire uno username!"
        elif not request.form.get("password"):
            return "Devi inserire una password!"
        
        username = request.form.get("username")
        password = request.form.get("password")
        
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            return "Password sbagliata!"
        
        session["user_id"] = rows[0]["id"]

        return redirect("/dashboard")
    
    else:
        return render_template("login.html")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if not (password == confirmation):
            return "Le password devono essere uguali!"
        
        if password == "" or confirmation == "" or username == "":
            return "Qualche campo è stato lasciato vuoto!"
        
        if len(rows) == 1:
            return "Questo account esiste di già! Fai il login :) "
        else:
            hashcode = generate_password_hash(password)
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, hashcode)

        return redirect("/")
    
    else:
        return render_template("sign_up.html")
    

@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    # Consumi medi trasporti
    consumo_macchina = 0.135
    consumo_motorino = 0.081
    consumo_aereo = 0.285
    
    # Consumi medi cibo
    consumo_carne = 0.06
    consumo_pasta = 0.01
    consumo_latticini = 0.11
    consumo_verdura = 0.006
    
    #Consumo medio energia
    consumo_energia = 0.5
    
    kgCO2_totali = 0
    percentuale = 0

    kgCO2 = None
    km_percorsi = None
    CO2trasporti = 0
    CO2cibo = 0
    CO2energia = 0
    obiettivo = None
    
    # Data oggi in formato YY/MM/DD
    data_creazione = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Query iniziali
    username = db.execute("SELECT username FROM users WHERE id = ? ", session["user_id"])[0]["username"]    
    obiettivo = db.execute("SELECT obiettivo FROM users WHERE id = ?", session["user_id"])[0]["obiettivo"]
    lista_emissioni = db.execute("SELECT strftime('%Y-%m-%d', data_creazione) AS data_creazione, tipo_emissione, kgCO2 FROM user_emissioni WHERE foreign_key_id = ? ORDER BY id DESC", session["user_id"])
    
    if request.method == "POST":
        if request.form.get("obiettivo"):
            obiettivo = int(request.form.get("obiettivo"))
            db.execute("UPDATE users SET obiettivo = ? WHERE id = ?", obiettivo, session["user_id"])
        
        if request.form.get("trasportiSelect"):
            mezzo = request.form.get("trasportiSelect")

            if request.form.get("kmPercorsi"):
                km_percorsi = int(request.form.get("kmPercorsi"))
                if mezzo == "Macchina":
                    kgCO2 = int(consumo_macchina * float(km_percorsi));
                elif mezzo == "Motorino":
                    kgCO2 = int(consumo_motorino * float(km_percorsi));
                elif mezzo == "Aereo":
                    kgCO2 = int(consumo_aereo * float(km_percorsi));
                else:
                    kgCO2 = None
            
            db.execute("INSERT INTO user_emissioni (foreign_key_id, tipo_emissione, kgCO2) VALUES (?, ?, ?)", session["user_id"], "Trasporti", kgCO2)
            
            return redirect("/dashboard") 
        
        if request.form.get("kWh"):
            kWh = float(request.form.get("kWh"))
            kgCO2 = int(kWh * consumo_energia)
            
            db.execute("INSERT INTO user_emissioni (foreign_key_id, tipo_emissione, kgCO2) VALUES (?, ?, ?)", session["user_id"], "Energia", kgCO2)
            
            return redirect("/dashboard")

        if request.form.get("ciboSelect"):
            tipo_cibo = request.form.get("ciboSelect")
            
            if request.form.get("gCibo"):
                gCibo = int(request.form.get("gCibo"))
                if tipo_cibo == "Carne":
                    kgCO2 = int(consumo_carne * float(gCibo))
                if tipo_cibo == "Pasta":
                    kgCO2 = int(consumo_pasta * float(gCibo))
                if tipo_cibo == "Latticini":
                    kgCO2 = int(consumo_latticini * float(gCibo))
                if tipo_cibo == "Verdura":
                    kgCO2 = int(consumo_verdura * float(gCibo))
            
            db.execute("INSERT INTO user_emissioni (foreign_key_id, tipo_emissione, kgCO2) VALUES (?, ?, ?)", session["user_id"], "Cibo", kgCO2)
            
            return redirect("/dashboard")
    
    if len(lista_emissioni) > 0:
        for item in lista_emissioni:
            if item.get("tipo_emissione") == "Trasporti" and item.get("kgCO2") != None:
                CO2trasporti += int(item.get("kgCO2"))
            if item.get("tipo_emissione") == "Energia" and item.get("kgCO2") != None:
                CO2energia += int(item.get("kgCO2"))
            if item.get("tipo_emissione") == "Cibo" and item.get("kgCO2") != None:
                CO2cibo += int(item.get("kgCO2"))
            
    # Grafico a torta
    labels = [CO2trasporti, CO2energia, CO2cibo]
    
    # Grafico a linee
    current_date = datetime.datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    
    primo_del_mese = datetime.datetime(current_year, current_month, 1)
    ultimo_del_mese = datetime.datetime(current_year, current_month, 1) + datetime.timedelta(days=30)
    
    rows = db.execute("SELECT data_creazione, kgCO2 FROM user_emissioni WHERE DATE(data_creazione) BETWEEN ? AND ? AND foreign_key_id = ?", primo_del_mese.strftime("%Y-%m-%d"), ultimo_del_mese.strftime("%Y-%m-%d"), session["user_id"])
    
    consumi_giornalieri_dict = {}
    
    for row in rows:
        data_creazione = row["data_creazione"]
        kgCO2 = row["kgCO2"]
        kgCO2_totali += kgCO2
        giorno_mese = (datetime.datetime.strptime(data_creazione, "%Y-%m-%d %H:%M:%S") - primo_del_mese).days
        if giorno_mese in consumi_giornalieri_dict and kgCO2 != None:
            consumi_giornalieri_dict[giorno_mese] += kgCO2
        else:
            if kgCO2 != None:
                consumi_giornalieri_dict[giorno_mese] = kgCO2
            
    consumi_giornalieri = [consumi_giornalieri_dict.get(giorno, 0) for giorno in range(30)]
    
    # Calcolo percentuale di completamento obiettivo
    if obiettivo != None:
        percentuale = int((kgCO2_totali/obiettivo)*100)
            
    return render_template("dashboard.html", lista_emissioni=lista_emissioni, labels=labels, consumi_giornalieri=consumi_giornalieri, username=username, obiettivo=obiettivo, percentuale=percentuale)
