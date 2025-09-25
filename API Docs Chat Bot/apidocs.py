from bs4 import BeautifulSoup
import requests
import json

url = "https://desk.zoho.com/DeskAPIDocument#Introduction"
print("Fetching:", url)
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

api_docs = []

# Extract all API sections
for section in soup.find_all("div", class_="totalmain"):
    # API Name
    title = section.find("h1").get_text(strip=True) if section.find("h1") else ""

    # API URL + Method (loop through resourceURI divs)
    api_url = ""
    api_method = ""
    for api_div in section.find_all("div", class_="resourceURI"):
        api_method_tag = api_div.find("strong")
        api_method = api_method_tag.get_text(strip=True) if api_method_tag else ""

        # Full text from div
        full_text = api_div.get_text(strip=True)

        # Remove the method part to get URL
        api_url = full_text.replace(api_method, "").strip()

    # API Description
    desc = section.find("p").get_text(strip=True) if section.find("p") else ""

    # Request Example (convert Tag -> text or HTML string)
    request_example_block = section.find("div", class_="sdk-box-content")
    request_example = request_example_block.get_text("\n", strip=True) if request_example_block else ""

    # OAuth Scope
    oauth_scope_tag = section.find("p", class_="resourceURI")
    oauth_scope = oauth_scope_tag.get_text(strip=True) if oauth_scope_tag else None

    # Response Example
    response_example = None
    resp_block = section.find("pre", class_="opt")
    if resp_block:
        response_example = resp_block.get_text(strip=True)

    # Query Params
    params = []
    for data in section.select(".productlist .data"):
        name = data.find("div", class_="data1")
        dtype = data.find("div", class_="data2")
        desc_block = data.find("div", class_="data3")
        if name and dtype and desc_block:
            params.append({
                "name": name.get_text(" ", strip=True),
                "data_type": dtype.get_text(" ", strip=True),
                "description": desc_block.get_text(" ", strip=True)
            })

    # Append API doc
    api_docs.append({
        "Api name": title,
        "Api URL": api_url,
        "Api Method": api_method,
        "Desc": desc,
        "OAuth Scope": oauth_scope,
        "Request Example": request_example,
        "Params": params,
        "Response Example": response_example
    })

# Save results to JSON
with open("api_docs.json", "w", encoding="utf-8") as f:
    json.dump(api_docs, f, ensure_ascii=False, indent=2)

print("✅ API docs scraped and saved to api_docs.json")
