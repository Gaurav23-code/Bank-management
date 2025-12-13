from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from db_config import get_connection
import os

app = Flask(__name__)

STAFF_PASSWORD = "admin123"   # Change if you want

@app.route("/")
def home():
    return render_template("main.html", action="home")

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        balance = request.form["balance"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO accounts (name, email, balance) VALUES (%s, %s, %s)",
            (name, email, balance)
        )
        conn.commit()
        account_no = cursor.lastrowid
        conn.close()

        return render_template("main.html", action="account_created", account_no=account_no)

    return render_template("main.html", action="create_account")

@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    if request.method == "POST":
        account_no = request.form["account_no"]
        amount = request.form["amount"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE account_no = %s",
            (amount, account_no)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("home"))

    return render_template("main.html", action="deposit")

@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    if request.method == "POST":
        account_no = request.form["account_no"]
        amount = request.form["amount"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE account_no = %s",
            (amount, account_no)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("home"))

    return render_template("main.html", action="withdraw")

@app.route("/balance", methods=["GET", "POST"])
def balance():
    bal = None
    if request.method == "POST":
        account_no = request.form["account_no"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT balance FROM accounts WHERE account_no = %s",
            (account_no,)
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            bal = result[0]

    return render_template("main.html", action="balance", balance=bal)

@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    if request.method == "POST":
        account_no = request.form["account_no"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM accounts WHERE account_no = %s",
            (account_no,)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("home"))

    return render_template("main.html", action="delete_account")

# -------- STAFF SECTION --------
@app.route("/staff_login", methods=["GET", "POST"])
def staff_login():
    error = None
    if request.method == "POST":
        password = request.form["password"]
        if password == STAFF_PASSWORD:
            return redirect(url_for("staff_dashboard"))
        else:
            error = "Invalid Password"
    return render_template("staff.html", action="login", error=error)

@app.route("/staff_dashboard")
def staff_dashboard():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT account_no, name, email, balance FROM accounts")
    accounts = cursor.fetchall()
    conn.close()
    return render_template("staff.html", action="dashboard", accounts=accounts)

# -------- DOWNLOAD PROJECT REPORT --------
@app.route("/download_report")
def download_report():
    return send_from_directory(
        directory=os.path.join(app.root_path, "reports"),
        path="ProjectReport.docx",
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)
