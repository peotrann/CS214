from flask import Flask, render_template, request
from .utils import filter_laws_for_web

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    results = []

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        if query:
            results = filter_laws_for_web(query)

    return render_template(
        "index.html",
        query=query,
        results=results
    )

@app.template_filter("comma")
def format_comma(value):
    try:
        return "{:,}".format(int(value))
    except (ValueError, TypeError):
        return value

if __name__ == "__main__":
    app.run(debug=True)
