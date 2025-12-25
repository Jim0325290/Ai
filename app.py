from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = "bad_secret_key"

def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_users():
    with open("users.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/", methods=["GET", "POST"])
def chat():
    reply = ""
    if request.method == "POST":
        user_input = request.form["text"]
        data = load_data()
        reply = data.get(
            user_input,
            "我不知道你在說什麼 / I don't know what you're talking about"
        )
    return render_template("chat.html", reply=reply)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = load_users()
        if users.get(request.form["username"]) == request.form["password"]:
            session["admin"] = True
            return redirect("/admin")
    return render_template("login.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin"):
        return redirect("/login")

    data = load_data()

    if request.method == "POST":
        key = request.form["key"]
        value = request.form["value"]
        if key:
            data[key] = value
            save_data(data)

    return render_template("admin.html", data=data)

@app.route("/delete/<key>")
def delete(key):
    if not session.get("admin"):
        return redirect("/login")

    data = load_data()
    if key in data:
        del data[key]
        save_data(data)

    return redirect("/admin")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
