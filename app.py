import datetime
import numpy as np
import yfinance as yf
import matplotlib
matplotlib.use('Agg')  # Prevent GUI errors in Flask
import matplotlib.pyplot as plt
import os
from flask import Flask, request, render_template, redirect, url_for, session, flash
from sklearn.linear_model import LinearRegression
from tinydb import TinyDB, Query
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

db = TinyDB("users.json")
User = Query()

# Ensure the 'static' directory exists for saving the stock chart
if not os.path.exists("static"):
    os.makedirs("static")

def predict_stock_price(ticker, future_date):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="2y")

        if df.empty:
            return f"❌ No data found for {ticker}. Stock may be delisted or ticker is incorrect.", None

        df['Date'] = df.index.map(datetime.datetime.toordinal)
        X = df[['Date']].values
        y = df['Close'].values

        model = LinearRegression()
        model.fit(X, y)

        future_date_ordinal = np.array([[datetime.datetime.strptime(future_date, "%Y-%m-%d").toordinal()]])
        predicted_price = model.predict(future_date_ordinal)[0]

        plt.figure(figsize=(8, 5))
        plt.scatter(df['Date'], df['Close'], color='blue', label="Historical Prices")
        plt.plot(df['Date'], model.predict(X), color='red', linestyle="dashed", label="Trend Line")
        plt.scatter(future_date_ordinal, predicted_price, color='green', s=100, marker="X", label="Predicted Price")

        plt.xlabel("Date")
        plt.ylabel("Stock Price (USD)")
        plt.title(f"{ticker} Stock Price Prediction for {future_date}")
        plt.legend()
        plt.grid()

        plt.savefig("static/stock_chart.png")
        plt.close()

        return round(predicted_price, 2), "static/stock_chart.png"

    except Exception as e:
        return f"⚠️ Error fetching data: {str(e)}", None

@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    future_date = None
    predicted_price = None
    image_path = None
    error_message = None

    if request.method == "POST":
        company_ticker = request.form["company"].strip().upper()
        future_date = request.form["future_date"]

        predicted_price, image_path = predict_stock_price(company_ticker, future_date)

        if isinstance(predicted_price, str):
            error_message = predicted_price
            predicted_price = None

    return render_template("index.html", future_date=future_date, predicted_price=predicted_price, image_path=image_path, error_message=error_message)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"].lower()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for("signup"))

        if db.search(User.email == email):
            flash("Email already registered!", "error")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        db.insert({"username": username, "email": email, "password": hashed_password})

        flash("Signup successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].lower()
        password = request.form["password"]

        user = db.search(User.email == email)
        if user and check_password_hash(user[0]["password"], password):
            session["user"] = email
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password!", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
