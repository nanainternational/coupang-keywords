from flask import Flask, request, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/related", methods=["GET"])
def get_related_keywords():
    keyword = request.args.get("q", "")
    if not keyword:
        return jsonify({"error": "Missing 'q' parameter"}), 400

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    driver.get(f"https://www.coupang.com/np/search?q={keyword}")
    time.sleep(2)

    keywords = []
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, "div.srp_relatedKeywords__DJiuk a")
        keywords = [el.text.strip() for el in elements if el.text.strip()]
    except Exception as e:
        print("❌ Error:", e)

    driver.quit()
    return jsonify({"keyword": keyword, "related": keywords})
