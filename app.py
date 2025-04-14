from flask import Flask, render_template, session, request, redirect, flash
from flask_session import Session
import uuid, os

app = Flask(__name__)
app.secret_key = "adam_project"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

file_save_location = "static/images"
allowed_types = [".png", ".jpg", ".jpeg"]
collection_of_something = []
@app.route("/")
def index():
    if "collection_of_something" not in session:
        session["collection_of_something"] = []
    return render_template("index.html", collection_of_something=session["collection_of_something"], file_location=file_save_location)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")

    elif request.method == "POST":
        if "collection_of_something" not in session:
            print("Clearing session data")
            session["collection_of_something"] = []

        name = request.form.get("name", "invalid")
        info = request.form.get("info", "invalid")
        uploaded_file = request.files['file']

        if uploaded_file.filename != '':
            extension = os.path.splitext(uploaded_file.filename)[1].lower()

            if extension in allowed_types:
                unique_name = f"{uuid.uuid4().hex}{extension}"
                filename = os.path.join(file_save_location, unique_name)
                uploaded_file.save(filename)
                session["collection_of_something"].append({"name": name, "info": info, "image": unique_name})
                session.modified = True
                flash("Added to collection", "message")
                return redirect("/")
            else:
                flash("Invalid file type, only .png, .jpg, .jpeg files allowed.", "error")
                return redirect("/add")


if __name__ == "__main__":
    app.run(debug=True)