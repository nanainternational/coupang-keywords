from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/related", methods=["GET"])
def get_related_keywords():
    keyword = request.args.get("q", "")
    if not keyword:
        return jsonify({"error": "Missing 'q' parameter"}), 400

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": "https://www.coupang.com/"
        }
        url = f"https://search.coupang.com/v1/api/suggestions?keyword={keyword}"
        response = requests.get(url, headers=headers)
        data = response.json()

        return jsonify({
            "keyword": keyword,
            "related": data.get("suggestions", [])
        })
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": "Failed to fetch suggestions."}), 500
