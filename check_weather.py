import time
import webbrowser
import urllib.parse
import pyautogui

# -------------------------------
# CONFIG
# -------------------------------
# Replace with your screen coordinates of the FIRST result link
# (to get them, run this script once, move mouse to the link, and note pyautogui.position())
FIRST_LINK_COORDS = (500, 320)   # <-- CHANGE THIS TO YOUR VALUES
OPEN_DELAY = 5.0                 # wait time for page to load
SEARCH_QUERY = "Tenkasi weather now"
# -------------------------------

# Fail-safe: moving mouse to top-left corner aborts the script
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.4

def main():
    # Open browser with search
    url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(SEARCH_QUERY)
    print("Opening:", url)
    webbrowser.open_new_tab(url)

    # wait for page to load
    print(f"Waiting {OPEN_DELAY} seconds for page to load...")
    time.sleep(OPEN_DELAY)

    # Move to first link and click
    print(f"Clicking at {FIRST_LINK_COORDS} ...")
    pyautogui.moveTo(FIRST_LINK_COORDS[0], FIRST_LINK_COORDS[1], duration=0.5)
    pyautogui.click()
    print("Done ✅")

if __name__ == "__main__":
    main()
