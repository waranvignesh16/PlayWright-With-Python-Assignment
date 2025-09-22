from bs4 import BeautifulSoup
import requests
import json

url = "https://desk.zoho.com/DeskAPIDocument#Introduction"
print(url)
response = requests.get(url)
#print(response)
soup = BeautifulSoup(response.text, "html.parser")
#print(soup)

api_docs = []
# Example: extract all endpoints
for section in soup.find_all("div", class_="totalmain"):
    title = section.find("h1").get_text(strip=True) if section.find("h1") else ""
    desc = section.find("p").get_text(strip=True) if section.find("p") else ""
    queryParam = section.find("div", class_="productlist").get_text(strip=True) if section.find("div", class_="productlist") else ""
    example = section.find("div", class_="examplereq").get_text(strip=True) if section.find("div", class_="examplereq") else ""

    api_docs.append({
        "title": title,
        "description": desc,
        "queryParam" : queryParam,
        "example": example
    })

print(api_docs)


# Save results to JSON file
with open("api_docs.json", "w", encoding="utf-8") as f:
    json.dump(api_docs, f, ensure_ascii=False, indent=2)

print("✅ API docs scraped and saved to api_docs.json")