from playwright.sync_api import sync_playwright

def get_tenkasi_weather_google():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114 Safari/537.36")
        page = context.new_page()
        page.goto("https://www.google.com/search?q=Tenkasi+weather+update")
        page.wait_for_timeout(4000)

        temp = page.locator("#wob_tm").inner_text()
        cond = page.locator("#wob_dc").inner_text()

        browser.close()
        return {"temperature_c": temp, "condition": cond}

print(get_tenkasi_weather_google())
