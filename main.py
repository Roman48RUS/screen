from flask import Flask, render_template, redirect, request, make_response, session, url_for, \
    send_from_directory

app = Flask(__name__, static_folder="/")
app.config["SECRET_KEY"] = "secret_key"


@app.route("/", methods=["GET", "POST"])
def index():
    print(url_for("static", filename="../css/bootstrap.css"))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
