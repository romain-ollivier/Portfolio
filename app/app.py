from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

# Obtenir le chemin absolu du répertoire parent
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, "templates"),
    static_folder=os.path.join(base_dir, "static")
)

# Charger les traductions
def load_translations(lang):
    try:
        with open(os.path.join(base_dir, 'translations', f'{lang}.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.route("/translations/<lang>.json")
def get_translations(lang):
    try:
        filepath = os.path.join(base_dir, 'translations', f'{lang}.json')
        with open(filepath, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({}), 404

@app.route("/")
def home():
    # Langue par défaut : français
    lang = request.args.get('lang', 'fr')
    texts = load_translations(lang)
    return render_template("home.html", texts=texts, lang=lang)

if __name__ == "__main__":
    app.run(debug=True)