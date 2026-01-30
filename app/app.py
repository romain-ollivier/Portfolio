from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

# Charger les traductions
def load_translations(lang):
    try:
        with open(f'translations/{lang}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.route("/")
def home():
    # Langue par défaut : français
    lang = request.args.get('lang', 'fr')
    texts = load_translations(lang)
    return render_template("home.html", texts=texts, lang=lang)

@app.route('/translations/<lang>.json')
def get_translations(lang):
    try:
        with open(f'translations/{lang}.json', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return {}, 404

if __name__ == "__main__":
    app.run(debug=True)