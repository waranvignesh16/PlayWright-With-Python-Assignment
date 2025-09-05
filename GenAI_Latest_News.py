from playwright.sync_api import sync_playwright

def scrape_genai_news():
    with sync_playwright() as p:
        # Step 1: Launch browser
        browser = p.chromium.launch(headless=False)  # set headless=True if you don't want UI
        page = browser.new_page()

        # Step 2: Go to Medium search page for GenAI
        page.goto("https://medium.com/search?q=GenAI")

        # Step 3: Grab the first article's full URL from `data-href`
        first_article = page.locator("article div[role='link']").first
        url = first_article.get_attribute("data-href")

        print(f"Opening article: {url}")

        # Step 4: Navigate to the article page
        page.goto(url)

        # Step 5: Extract title and content
        title = page.locator("h1").inner_text()
        paragraphs = page.locator("article p").all_inner_texts()
        content = "\n\n".join(paragraphs)

        # Step 6: Save to file
        with open("genai_news.txt", "w", encoding="utf-8") as f:
            f.write(title + "\n\n" + content)

        print("✅ Article saved to genai_news.txt")

        browser.close()


if __name__ == "__main__":
    scrape_genai_news()
