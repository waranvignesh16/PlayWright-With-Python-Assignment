#!/usr/bin/env python3
"""
mom_auto_playwright.py

- Reads formatted MoM from Google Sheets (bold/italic preserved)
- Rephrases using OpenAI (new API >=1.0)
- Converts Markdown -> WhatsApp formatting
- Sends to a WhatsApp group via Playwright (persistent login)
- Saves a local timestamped copy
"""

import os
import re
import time
from datetime import datetime
from typing import List

# Google Sheets API
from google.oauth2 import service_account
from googleapiclient.discovery import build

# OpenAI (>=1.0)
from openai import OpenAI
client = OpenAI()

# Playwright
from playwright.sync_api import sync_playwright

# ---------------- CONFIG ----------------
SERVICE_ACCOUNT_FILE = "gsa-credentials.json"
SPREADSHEET_ID = "1Q1M-zmc0HkpEAW0Fp_i8GVgAqKfcNYTqBeSHS4lyc3c"
SHEET_NAME = "DSM"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client.api_key = OPENAI_API_KEY
OPENAI_MODEL = "gpt-3.5-turbo-instruct"

WHATSAPP_GROUP_NAME = "SE - AI-B2 - 1"
WA_STORAGE = "wa_state.json"
OUTPUT_DIR = "."
MAX_WA_CHUNK = 4000
# -----------------------------------------

# ---------- Google Sheets (preserve formatting) ----------
def get_sheets_service(sa_file: str):
    creds = service_account.Credentials.from_service_account_file(
        sa_file, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    service = build("sheets", "v4", credentials=creds)
    return service

def fetch_sheet_grid(service, spreadsheet_id: str, sheet_name: str):
    res = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        ranges=[sheet_name],
        includeGridData=True
    ).execute()
    sheets = res.get("sheets", [])
    if not sheets:
        return []
    data = sheets[0].get("data", [])
    if not data:
        return []
    return data[0].get("rowData", [])

def format_cell_to_markdown(cell: dict) -> str:
    text = cell.get("userEnteredValue", {}).get("stringValue", "")
    if not text:
        return ""

    runs = cell.get("textFormatRuns")
    if runs:
        runs_sorted = sorted(runs, key=lambda r: r.get("startIndex", 0))
        parts = []
        for i, run in enumerate(runs_sorted):
            start = run.get("startIndex", 0)
            end = runs_sorted[i + 1].get("startIndex", len(text)) if i + 1 < len(runs_sorted) else len(text)
            substring = text[start:end]
            style = run.get("format", {}).get("textFormat", {})
            bold = style.get("bold", False)
            italic = style.get("italic", False)
            if bold and italic:
                parts.append(f"***{substring}***")
            elif bold:
                parts.append(f"**{substring}**")
            elif italic:
                parts.append(f"*{substring}*")
            else:
                parts.append(substring)
        return "".join(parts)
    else:
        fmt = cell.get("userEnteredFormat", {}).get("textFormat", {})
        bold = fmt.get("bold", False)
        italic = fmt.get("italic", False)
        s = text
        if bold and italic:
            return f"***{s}***"
        if bold:
            return f"**{s}**"
        if italic:
            return f"*{s}*"
        return s

def sheet_to_markdown(service, spreadsheet_id: str, sheet_name: str) -> str:
    row_data = fetch_sheet_grid(service, spreadsheet_id, sheet_name)
    lines = []
    for row in row_data:
        vals = row.get("values", [])
        cell_texts = []
        for cell in vals:
            md = format_cell_to_markdown(cell)
            if md:
                cell_texts.append(md)
        if cell_texts:
            lines.append(" ".join(cell_texts))
    return "\n\n".join(lines)

# ---------- OpenAI rephrase ----------
def rephrase_with_openai_markdown(text: str, model: str = OPENAI_MODEL) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Rephrase the following meeting notes into a concise, professional Minutes of Meeting format. Keep any markdown-style bold/italic markers intact."},
        {"role": "user", "content": f"Raw notes:\n{text}\n\nRewrite as: Title, Summary, Key Points (bulleted), Action Items (bulleted). Preserve markdown formatting."}
    ]

    #resp = client.chat.completions.create(
     #   model=model,
      #  messages=messages,
       # temperature=0.2,
        #max_tokens=1200
    #)
    return "demo please ignore.. "#resp.choices[0].message.content.strip()

# ---------- Convert Markdown -> WhatsApp formatting ----------
def markdown_to_whatsapp(md_text: str) -> str:
    text = md_text
    text = re.sub(r"\*\*\*([^\*]+)\*\*\*", r'*_\1_*', text)
    text = re.sub(r"\*\*([^\*]+)\*\*", r'*\1*', text)
    text = re.sub(r"(?<!\*)\*([^\*]+)\*(?!\*)", r'_\1_', text)
    return text

# ---------- Chunking for WhatsApp ----------
def chunk_text(text: str, max_len: int = MAX_WA_CHUNK) -> List[str]:
    chunks = []
    while text:
        if len(text) <= max_len:
            chunks.append(text)
            break
        idx = text.rfind("\n\n", 0, max_len)
        if idx == -1:
            idx = text.rfind("\n", 0, max_len)
        if idx == -1:
            idx = text.rfind(" ", 0, max_len)
        if idx == -1:
            idx = max_len
        chunk = text[:idx].strip()
        chunks.append(chunk)
        text = text[idx:].strip()
    return chunks

# ---------- Playwright send to WhatsApp ----------
def send_whatsapp_playwright(message: str, group_name: str, storage_state: str = WA_STORAGE):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        if os.path.exists(storage_state):
            context = browser.new_context(storage_state=storage_state)
            print("Loaded existing WhatsApp login state.")
        else:
            context = browser.new_context()
        
        page = context.new_page()
        page.goto("https://web.whatsapp.com")

        if not os.path.exists(storage_state):
            print("Scan QR code for WhatsApp Web (you have 2 minutes)...")
            page.wait_for_selector("span[title]", timeout=120_000)
            print("QR scanned. Saving login state...")
            context.storage_state(path=storage_state)
            print(f"Saved state to {storage_state}")
        else:
            page.wait_for_selector("span[title]", timeout=30_000)

        # Select WhatsApp group
        group_sel = f"span[title='{group_name}']"
        print(f"group_sel==>{group_sel}")
        try:
            page.locator(group_sel).click(timeout=15000)
        except Exception:
            anchors = page.locator("div[role='row'] span[title]")
            found = False
            for i in range(anchors.count()):
                t = anchors.nth(i).inner_text()
                if group_name.lower() in t.lower():
                    anchors.nth(i).click()
                    found = True
                    break
            if not found:
                raise RuntimeError(f"Could not find WhatsApp group named '{group_name}'.")

        # Locate input box
        input_selectors = [
            "div[title='Type a message']",
            "div[contenteditable='true'][data-tab='1']",
            "div[contenteditable='true']"
        ]
        msg_box = None
        for sel in input_selectors:
            if page.locator(sel).count() > 0:
                msg_box = page.locator(sel).first
                break
        if not msg_box:
            raise RuntimeError("Could not locate WhatsApp message input box.")

        # Send in chunks
        chunks = chunk_text(message, MAX_WA_CHUNK)
        print(f"chunks==>{chunks}")
        print(f"page==>{page}")
        for chunk in chunks:
            msg_box.click()
            page.keyboard.insert_text(chunk)
            page.keyboard.press("Enter")
            time.sleep(0.8)

        print("✅ Message sent to WhatsApp group.")
        context.close()
        browser.close()

# ---------- Main pipeline ----------
def main():
    print("1) Connecting to Google Sheets...")
    service = get_sheets_service(SERVICE_ACCOUNT_FILE)

    print("2) Reading sheet and extracting formatted text...")
    md_text = sheet_to_markdown(service, SPREADSHEET_ID, SHEET_NAME)
    if not md_text.strip():
        print("No text found in the sheet. Exiting.")
        return

    print("=== Raw extracted (markdown) ===")
    print(md_text[:1000] + ("..." if len(md_text) > 1000 else ""))

    print("\n3) Rephrasing via OpenAI...")
    polished_md = rephrase_with_openai_markdown(md_text)
    print("=== Rephrased (markdown) preview ===")
    print(polished_md[:1200] + ("..." if len(polished_md) > 1200 else ""))

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_md = os.path.join(OUTPUT_DIR, f"MoM_{ts}.md")
    with open(filename_md, "w", encoding="utf-8") as f:
        f.write(polished_md)
    print(f"Saved rephrased markdown to {filename_md}")

    wa_text = markdown_to_whatsapp(polished_md)
    print("\n4) Sending to WhatsApp group...")
    send_whatsapp_playwright(wa_text, WHATSAPP_GROUP_NAME, storage_state=WA_STORAGE)

    print("All done.")

if __name__ == "__main__":
    main()
