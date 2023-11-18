# dictionary-api-python-flask/app.py
from flask import Flask, request, jsonify, render_template
from model.dbHandler import match_exact, match_like

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", response={"words": []})  # Initialize response with an empty list

@app.route("/dict", methods=['GET', 'POST'])
def dictionary():
    if request.method == 'POST':
        word = request.form.get('word')
        definitions = match_exact(word)

        if definitions:
            response = {"status": "success", "words": [{"status": "success", "data": definitions, "word": word}]}
        else:
            definitions = match_like(word)
            if definitions:
                response = {"status": "partial", "words": [{"status": "partial", "data": definitions, "word": word}]}
            else:
                response = {"status": "error", "words": [{"status": "error", "data": "word not found", "word": word}]}

        return jsonify(response)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
