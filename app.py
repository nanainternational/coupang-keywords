from flask import Flask, request, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    # 셀레니움 크롬 실행 옵션 설정
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    # 쿠팡 검색 페이지 접속
    driver.get(f"https://www.coupang.com/np/search?q={keyword}")

    # 연관검색어 요소가 로드될 때까지 최대 5초 기다림
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.srp_relatedKeywords__DJiuk a"))
        )
    except:
        print("❌ 연관검색어 로딩 실패")

    # 연관검색어 추출
    keywords = []
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, "div.srp_relatedKeywords__DJiuk a")
        keywords = [el.text.strip() for el in elements if el.text.strip()]
    except Exception as e:
        print("❌ Error:", e)

    driver.quit()
    return jsonify({"keyword": keyword, "related": keywords})
