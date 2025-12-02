from playwright.sync_api import sync_playwright
import time

def verify_nutriscore_filter():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to login page
        print("Navigating to login page...")
        page.goto("http://127.0.0.1:5000/login")

        # Login if needed (might be redirected to index if already authenticated or if login is bypassed in dev)
        # Based on routes.py, /login requires authentication only if session not set.
        # But wait, routes.py has Microsoft SSO.
        # However, there is a master login route /master-login

        print("Navigating to master login...")
        page.goto("http://127.0.0.1:5000/master-login")

        # Fill login form
        print("Filling login form...")
        page.fill('input[name="username"]', "innocatmaster23568")
        page.fill('input[name="password"]', "Villa23568hafer23568!")

        # Click sign in
        print("Clicking Sign In...")
        page.click('button:has-text("Sign In")')

        # Wait for redirect to index
        page.wait_for_url("http://127.0.0.1:5000/")
        print("Logged in successfully.")

        # Navigate to Innovation Catalog
        print("Navigating to Innovation Catalog...")
        page.goto("http://127.0.0.1:5000/catalog")

        # Wait for filters to load
        print("Waiting for filters...")
        page.wait_for_selector('.filters-section')

        # Click on Nutri-Score filter header
        print("Clicking Nutri-Score filter...")
        # Find header with data-filter="nutri_score"
        page.click('[data-filter="nutri_score"]')

        # Wait for options to appear
        time.sleep(1)

        # Take screenshot of open filter
        print("Taking screenshot...")
        page.screenshot(path="verification/nutriscore_filter_open.png")

        # Click on Option "A"
        print("Selecting Nutri-Score A...")
        page.click('button[data-filter="nutri_score"][data-value="A"]')

        # Wait for page reload/filter application
        time.sleep(2)

        # Take screenshot of filtered results
        print("Taking filtered screenshot...")
        page.screenshot(path="verification/nutriscore_filtered_A.png")

        browser.close()

if __name__ == "__main__":
    try:
        verify_nutriscore_filter()
        print("Verification script completed.")
    except Exception as e:
        print(f"Verification failed: {e}")
