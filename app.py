from flask import Flask, render_template, session
from flask_session import Session

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



if __name__ == "__main__":
    app.run(debug=True)