from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import time
import yfinance as yf

# Obtenir le chemin absolu du répertoire parent
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, "templates"),
    static_folder=os.path.join(base_dir, "static")
)

CAC40_CACHE = {"expires_at": 0, "data": None}

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

@app.route("/skills/data")
def skills_data():
    return render_template("skills/data.html")

@app.route("/api/cac40")
def cac40_data():
    now = time.time()
    if CAC40_CACHE["data"] and CAC40_CACHE["expires_at"] > now:
        return jsonify(CAC40_CACHE["data"])

    try:
        history = yf.download(
            "^FCHI",
            period="1mo",
            interval="1d",
            auto_adjust=False,
            progress=False,
            threads=False,
        )
    except Exception as error:
        app.logger.warning("Yahoo Finance request failed: %s", error)
        return jsonify({"error": "Unable to retrieve CAC 40 data from Yahoo Finance."}), 502

    if history.empty or "Close" not in history:
        return jsonify({"error": "Yahoo Finance returned no CAC 40 data."}), 502

    close_values = history["Close"]
    if hasattr(close_values, "columns"):
        close_values = close_values.iloc[:, 0]

    data = {
        "meta": {"symbol": "^FCHI", "source": "Yahoo Finance"},
        "values": [
            {"date": index.strftime("%Y-%m-%d"), "close": float(value)}
            for index, value in close_values.items()
            if value == value
        ],
    }
    CAC40_CACHE.update({"data": data, "expires_at": now + 900})
    return jsonify(data)

@app.route("/skills/pm")
def skills_pm():
    return render_template("skills/pm.html")

@app.route("/skills/automation")
def skills_automation():
    return render_template("skills/automation.html")

if __name__ == "__main__":
    app.run(debug=True)