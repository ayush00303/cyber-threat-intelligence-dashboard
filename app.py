from flask import Flask, render_template, request, redirect, session, Response
import sqlite3
import requests
import datetime
import ipaddress

app = Flask(__name__)
app.secret_key = "secret123"


# -------------------------------
# DATABASE INITIALIZATION
# -------------------------------

def init_db():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        country TEXT,
        risk_score INTEGER,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# -------------------------------
# RISK CALCULATION
# -------------------------------

def calculate_risk(country):

    high_risk = ["Russia","China","Iran","North Korea"]

    if country == "Unknown":
        return 10

    if country in high_risk:
        return 70

    return 20


# -------------------------------
# HOME
# -------------------------------

@app.route("/")
def home():

    if "user" in session:
        return redirect("/dashboard")

    return redirect("/register")


# -------------------------------
# REGISTER
# -------------------------------

@app.route("/register", methods=["GET","POST"])
def register():

    if "user" in session:
        return redirect("/dashboard")

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
        "INSERT INTO users(username,email,password) VALUES(?,?,?)",
        (username,email,password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# -------------------------------
# LOGIN
# -------------------------------

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session["user"] = user[1]
            return redirect("/dashboard")

        else:
            return "Incorrect email or password"

    return render_template("login.html")


# -------------------------------
# DASHBOARD
# -------------------------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scans")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE risk_score>50")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE risk_score<=50")
    low = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total=total,
        high=high,
        low=low
    )


# -------------------------------
# SCANNER
# -------------------------------

@app.route("/scanner", methods=["GET","POST"])
def scanner():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        ip = request.form["ip"]

        try:

            ip_obj = ipaddress.ip_address(ip)

            # Private IP detection
            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved:
                country = "Private / Reserved IP"
                risk_score = 0

            else:

                response = requests.get(
                    f"http://ip-api.com/json/{ip}",
                    timeout=5
                )

                data = response.json()

                country = data.get("country","Unknown")

                risk_score = calculate_risk(country)

            # Save scan
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute(
            "INSERT INTO scans(ip,country,risk_score,date) VALUES(?,?,?,?)",
            (ip,country,risk_score,str(datetime.datetime.now()))
            )

            conn.commit()
            conn.close()

            return render_template(
                "result.html",
                ip=ip,
                country=country,
                risk_score=risk_score
            )

        except:
            return "Invalid IP Address"

    return render_template("index.html")


# -------------------------------
# HISTORY
# -------------------------------

@app.route("/history")
def history():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scans ORDER BY id DESC")
    data = cursor.fetchall()

    conn.close()

    return render_template("history.html",scans=data)


# -------------------------------
# STATISTICS
# -------------------------------

@app.route("/statistics")
def statistics():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scans")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE risk_score>=70")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE risk_score<70")
    low = cursor.fetchone()[0]

    conn.close()

    return render_template(
    "statistics.html",
    total=total,
    high=high,
    low=low
    )


# -------------------------------
# EXPORT CSV
# -------------------------------

@app.route("/export")
def export():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scans")
    data = cursor.fetchall()

    conn.close()

    def generate():

        yield "ID,IP,Country,Risk Score,Date\n"

        for row in data:
            yield f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}\n"

    return Response(
    generate(),
    mimetype="text/csv",
    headers={"Content-Disposition":"attachment; filename=report.csv"}
    )


# -------------------------------
# OTHER PAGES
# -------------------------------

@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/admin")
def admin():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template("admin.html",users=users)


@app.route("/map")
def map():
    return render_template("map.html")


# -------------------------------
# CHANGE PASSWORD
# -------------------------------

@app.route("/change-password", methods=["GET","POST"])
def change_password():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        old = request.form["old_password"]
        new = request.form["new_password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (session["user"],old)
        )

        user = cursor.fetchone()

        if user:

            cursor.execute(
            "UPDATE users SET password=? WHERE username=?",
            (new,session["user"])
            )

            conn.commit()
            conn.close()

            return "Password Updated Successfully"

        else:
            return "Old password incorrect"

    return render_template("change_password.html")


# -------------------------------
# LOGOUT
# -------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


@app.route("/forgot")
def forgot():
    return render_template("forgot.html")


# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)