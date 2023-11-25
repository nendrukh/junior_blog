from flask import Flask, render_template

app = Flask(__name__)


@app.route("/hi")
def hello():
    return "Hello11"


@app.route("/html")
def site():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
