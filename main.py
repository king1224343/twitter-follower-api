from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
import re

app = FastAPI()

@app.get("/")
def read_root(username: str = Query(..., description="Twitter username")):
    api_key = "7d28ca6d4f92411f1e5cf46952b9d26e"  # 你的 ScraperAPI key
    url = f"https://twitter.com/{username.lstrip('@')}"
    scraper_url = f"http://api.scraperapi.com?api_key={api_key}&url={url}"

    response = requests.get(scraper_url, headers={"User-Agent": "Mozilla/5.0"})
    html = response.text

    # 打印返回内容用于调试（部署后可注释掉）
    print("🔍 ScraperAPI 返回内容开始：")
    print(html[:1000])  # 只打印前 1000 字符防止过长
    print("🔍 ScraperAPI 返回内容结束")

    # 检查是否被拦截或跳转了
    if "captcha" in html.lower() or "cloudflare" in html.lower() or "Access Denied" in html:
        return JSONResponse(content={
            "username": username,
            "followers_count": "Blocked or Captcha page returned"
        })

    # 用 BeautifulSoup 提取页面文字
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    # 尝试匹配“Followers”字样前面的数字
    match = re.search(r"([\d\.,]+[MK]?)\s*Followers", text, re.IGNORECASE)
    followers = match.group(1) if match else "Not found"

    return JSONResponse(content={
        "username": username,
        "followers_count": followers
    })
