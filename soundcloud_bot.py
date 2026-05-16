from playwright.sync_api import sync_playwright
import time
import random

# The SoundCloud song you want to loop
SONG_URL = "https://soundcloud.com/mancouver/mancouver-liquicity-festival" 

def run():
    with sync_playwright() as p:
        # Launch browser. headless=False means you can visually watch it happen.
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to SoundCloud...")
        page.goto(SONG_URL)

        # 1. Handle SoundCloud's Cookie Popup (Only needs to be done once)
        try:
            print("Checking for cookie popup...")
            page.locator("#onetrust-accept-btn-handler").click(timeout=10000)
            page.locator("#onetrust-consent-sdk").wait_for(state="hidden", timeout=10000)
            print("Cookie popup accepted.")
        except Exception as e:
            print("No cookie popup found or timeout, continuing.")

        # 2. Loop the play and refresh process 5 times
        for i in range(5):
            print(f"\n--- Playthrough {i + 1} of 5 ---")
            
            try:
                # wait a bit for page to load and play button to potentially be visible
                page.locator("a[title='Play']:visible").first.wait_for(timeout=5000)
            except Exception:
                pass

            try:
                if page.locator(".modal__closeButton").is_visible():
                    print("Closing auth modal...")
                    page.locator(".modal__closeButton").click()
            except Exception:
                pass

            # Wait for the play or pause button to be ready
            try:
                play_or_pause = page.locator("a[title='Play']:visible, a[title='Pause']:visible").first
                play_or_pause.wait_for(timeout=10000)
                
                if page.locator("a[title='Play']:visible").count() > 0:
                    print("Clicking Play...")
                    page.locator("a[title='Play']:visible").first.evaluate("node => node.click()")
                else:
                    print("Track is already playing.")
            except Exception as e:
                print("Play/Pause button not found.")

            # Generate a random number between 60 and 300, with 10 decimal places
            sleep_time = round(random.uniform(60, 300), 10)
            print(f"Listening for {sleep_time} seconds...")
            time.sleep(sleep_time)

            # Refresh the page (unless it is the very last loop)
            if i < 4:
                print("Refreshing the page...")
                page.reload()

        print("\nDone! Completed 5 loops. Closing browser.")
        browser.close()

if __name__ == "__main__":
    run()