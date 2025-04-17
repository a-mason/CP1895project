from flask import Flask, render_template, session, request, redirect, flash
from flask_session import Session
import uuid, os, random

app = Flask(__name__)
app.secret_key = "adam_project"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
Session(app)

file_save_location = "static/images"
allowed_types = [".png", ".jpg", ".jpeg"]
os.makedirs(file_save_location, exist_ok=True)
@app.route("/")
def index():
    if "characters" not in session:
        session["characters"] = []
    if "boss_hp" not in session:
        session["boss_hp"] = 100
    return render_template("index.html", characters=session["characters"], boss_hp=session["boss_hp"], file_location=file_save_location)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")

    elif request.method == "POST":
        if "characters" not in session:
            print("Clearing session data")
            session["characters"] = []

        name = request.form.get("name", "invalid")
        uploaded_file = request.files["file"]

        if uploaded_file.filename != "":
            extension = os.path.splitext(uploaded_file.filename)[1].lower()

            if extension in allowed_types:
                unique_name = f"{uuid.uuid4().hex}{extension}"
                filename = os.path.join(file_save_location, unique_name)
                uploaded_file.save(filename)
                session["characters"].append({
                    "characterid": uuid.uuid4().hex,
                    "name": name,
                    "image": unique_name,
                    "hp": 20})
                session.modified = True
                flash("Added to collection", "message")
                return redirect("/")
            else:
                flash("Invalid file type", "error")
                flash("Only .png, .jpg, .jpeg files allowed.", "error")
                return redirect("/add")

@app.route("/battle")
def battle():
    if "boss_hp" not in session:
        session["boss_hp"] = 100
    if "turn_taken" not in session:
        session["turn_taken"] = []

    return render_template("battle.html",
                           characters=session["characters"],
                           file_location=file_save_location,
                           boss_hp=session["boss_hp"])

@app.route("/remove/<characterid>", methods=["POST"])
def remove(characterid):
    for character in session["characters"]:
        if character["characterid"] == characterid:
            session["characters"].remove(character)
            session.modified = True
            flash("Character removed", "message")
            break

    return redirect("/")

@app.route("/attack/<characterid>", methods=["POST"])
def attack(characterid):
    if "characters" not in session:
        flash("No characters available", "error")
        return redirect("/battle")

    for character in session["characters"]:
        if character["characterid"] == characterid:
            attacker = character
            break

    damage = random.randint(1, 5)
    session["boss_hp"] = max(session.get("boss_hp", 100) - damage, 0)
    flash(f"{attacker["name"]} dealt {damage} damage to the boss!", "attack")

    counter_damage = random.randint(1, 5)
    attacker["hp"] = max(attacker["hp"] - counter_damage, 0)
    flash(f"The boss counterattacked for {counter_damage} damage to {attacker["name"]}!", "counter")


    if attacker["hp"] <= 0:
        flash(f"{attacker["name"]} has fainted!", "fainted")
        return redirect("/battle")

    session.modified = True
    return redirect("/battle")

@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)