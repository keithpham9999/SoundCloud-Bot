from playwright.sync_api import sync_playwright

SONG_URL = "https://soundcloud.com/mancouver/mancouver-liquicity-festival" 

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(SONG_URL)
    page.wait_for_timeout(5000)
    
    with open("page_source.html", "w") as f:
        f.write(page.content())
        
    browser.close()
