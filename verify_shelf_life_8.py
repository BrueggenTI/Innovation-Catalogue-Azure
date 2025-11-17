
import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Login
            print("Navigating to login page...")
            await page.goto("http://localhost:5000/master-login")
            await page.fill('input[name="username"]', "innocatmaster23568")
            await page.fill('input[name="password"]', "Villa23568hafer23568!")
            await page.click('button[type="submit"]')
            # Corrected the selector to match the actual h1 text
            await page.wait_for_selector("h1:has-text('Welcome to the Brüggen Innovation Catalogue')", timeout=15000)
            print("Login successful.")

            # Set the session cookie to show unapproved recipes
            print("Disabling 'hide unapproved recipes' filter...")
            await context.add_cookies([{'name': 'hide_unapproved_recipes', 'value': 'false', 'url': 'http://localhost:5000'}])
            print("Filter disabled.")

            # Navigate to the add recipe page
            print("Navigating to add recipe page...")
            await page.goto("http://localhost:5000/add-recipe")
            await page.wait_for_selector("h2:has-text('Create New Recipe')")
            print("On add recipe page.")

            # Simulate file upload for batch processing
            print("Simulating batch file upload...")
            dummy_file_path = "/home/jules/dummy_excel_file.xlsx"
            if not os.path.exists(dummy_file_path):
                with open(dummy_file_path, "w") as f:
                    f.write("dummy content")

            await page.set_input_files('input[type="file"]', [dummy_file_path])

            # Wait for the recipe carousel to appear
            await page.wait_for_selector("#recipe-carousel .carousel-item", timeout=45000)
            print("Recipe carousel loaded.")

            # Publish the first recipe in the carousel
            print("Publishing the first recipe...")
            await page.click("#publish-all-btn")

            # Wait for the success alert and redirection
            await page.wait_for_selector(".alert-success:has-text('Your new recipe has been successfully published')", timeout=20000)
            print("Recipe published successfully. Redirected to catalog.")

            # Verify the new product is in the catalog
            print("Verifying recipe in catalog...")
            # This is the name from the dummy data returned by the backend
            product_card_selector = "h5.card-title:has-text('Recipe from dummy_excel_file.xlsx')"
            await page.wait_for_selector(product_card_selector, timeout=15000)
            print("Found new recipe card in the catalog.")

            # Click on the new product to go to the detail page
            await page.click(product_card_selector)
            await page.wait_for_selector("h1:has-text('Recipe from dummy_excel_file.xlsx')")
            print("Navigated to product detail page.")

            # Verify the shelf life is displayed correctly
            storage_conditions_section = page.locator("h3:has-text('Storage Conditions') + div")
            shelf_life_text = await storage_conditions_section.inner_text()

            expected_shelf_life = "12 months (365 days)" # From the dummy data for "Traditional Muesli"
            if expected_shelf_life in shelf_life_text:
                print(f"SUCCESS: Found correct shelf life info: '{shelf_life_text}'")
            else:
                raise Exception(f"FAILED: Shelf life info is incorrect. Found: '{shelf_life_text}', Expected to contain: '{expected_shelf_life}'")

            # Take a final screenshot
            os.makedirs("/home/jules/verification", exist_ok=True)
            screenshot_path = "/home/jules/verification/final_verification_success.png"
            await page.screenshot(path=screenshot_path)
            print(f"Final success screenshot saved to {screenshot_path}")


        except Exception as e:
            print(f"An error occurred: {e}")
            os.makedirs("/home/jules/verification", exist_ok=True)
            await page.screenshot(path="/home/jules/verification/verification_error.png")
            raise
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
