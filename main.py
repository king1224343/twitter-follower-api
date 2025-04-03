from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
import re

app = FastAPI()

@app.get("/")
def read_root(username: str = Query(..., description="Twitter username")):
    api_key = "7d28ca6d4f92411f1e5cf46952b9d26e"
    url = f"https://twitter.com/{username.lstrip('@')}"
    scraper_url = f"http://api.scraperapi.com?api_key={api_key}&url={url}"

    response = requests.get(scraper_url, headers={"User-Agent": "Mozilla/5.0"})
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    match = re.search(r"([\d\.,]+[MK]?)\s*Followers", text)
    followers = match.group(1) if match else "Not found"

    return JSONResponse(content={
        "username": username,
        "followers_count": followers
    })