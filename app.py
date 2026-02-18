from flask import Flask, render_template, request
from flask import Response
import requests
import sqlite3
import datetime
import ipaddress

app = Flask(__name__)

# Create database table
# -------------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
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


# Risk Calculation Logic

def calculate_risk(country):
    score = 0
    high_risk_countries = ["Russia", "China", "Iran", "North Korea"]

    if country == "Unknown":
        score += 10
    elif country in high_risk_countries:
        score += 70
    else:
        score += 20

    return score


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ip = request.form["ip"]

        #  Private IP Detection
        try:
            ip_obj = ipaddress.ip_address(ip)

            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved:
                country = "Private / Reserved IP"
                risk_score = 0

                # Save in DB
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO scans (ip, country, risk_score, date) VALUES (?, ?, ?, ?)",
                    (ip, country, risk_score, str(datetime.datetime.now()))
                )
                conn.commit()
                conn.close()

                return render_template("result.html",
                                       ip=ip,
                                       country=country,
                                       risk_score=risk_score)
        except:
            return "Invalid IP Address"

        #  Public IP API Call
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}")
            data = response.json()

            country = data.get("country", "Unknown")
            risk_score = calculate_risk(country)

            # Save in DB
            
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO scans (ip, country, risk_score, date) VALUES (?, ?, ?, ?)",
                (ip, country, risk_score, str(datetime.datetime.now()))
            )
            conn.commit()
            conn.close()

            return render_template("result.html",
                                   ip=ip,
                                   country=country,
                                   risk_score=risk_score)

        except:
            return "Error fetching data from API"

    return render_template("index.html")



# History Page

@app.route("/history")
def history():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scans ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return render_template("history.html", scans=data)


#Add professional API route

@app.route("/api/scan/<ip>")
def api_scan(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)

        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved:
            return {
                "ip": ip,
                "country": "Private / Reserved IP",
                "risk_score": 0
            }

        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()

        country = data.get("country", "Unknown")
        risk_score = calculate_risk(country)

        return {
            "ip": ip,
            "country": country,
            "risk_score": risk_score
        }

    except:
        return {
            "error": "Invalid IP address"
        }


@app.route("/export")
def export_csv():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scans ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()

    def generate():
        yield "ID,IP,Country,Risk Score,Date\n"
        for row in data:
            yield f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}\n"

    return Response(generate(),
                    mimetype="text/csv",
                    headers={"Content-Disposition":
                             "attachment; filename=scan_report.csv"})


#statistics page

@app.route("/statistics")
def statistics():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scans")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE risk_score >= 70")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE risk_score < 70")
    low = cursor.fetchone()[0]

    conn.close()

    return render_template("statistics.html",
                           total=total,
                           high=high,
                           low=low)


if __name__ == "__main__":
    app.run(debug=True)
