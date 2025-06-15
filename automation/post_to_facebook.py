from playwright.sync_api import sync_playwright
import time
import os


def save_session(email):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.facebook.com/login")

        print(f"👉 Please log in manually for: {email}")
        print("⏳ You have 60 seconds...")
        time.sleep(60)

        session_path = f"sessions/{email.replace('@', '_').replace('.', '_')}.json"
        context.storage_state(path=session_path)
        print(f"✅ Session saved: {session_path}")
        browser.close()


# def login_and_post(email, title, description, price, image_path, location):
def login_and_post(email, title, description, price, image_path):
    session_file = f"sessions/{email.replace('@', '_').replace('.', '_')}.json"
    if not os.path.exists(session_file):
        raise Exception(
            f"❌ Session not found. Run save_session('{email}') first.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=session_file)
        page = context.new_page()

        print("🌐 Opening Marketplace listing page...")
        page.goto("https://www.facebook.com/marketplace/create/item",
                  timeout=60000)

        try:
            print("📸 Uploading image first...")
            image_input = page.locator("input[type='file'][accept*='image']")
            image_input.set_input_files(image_path)
            page.wait_for_timeout(2000)  # Wait for UI to update after upload

            print("📝 Filling Title...")
            # Find all visible text inputs that are empty and not in the header
            text_inputs = page.locator("input[type='text']")
            title_input = None

            for i in range(text_inputs.count()):
                el = text_inputs.nth(i)
                # Check if visible and empty
                if el.is_visible() and el.input_value() == "":
                    # Optionally, skip if it's in the header (search bar)
                    # You can check its position on the page
                    box = el.bounding_box()
                    if box and box['y'] > 100:  # Skip inputs at the very top
                        title_input = el
                        break

            if not title_input:
                all_inputs = page.locator("input")
                print(
                    f"Found {all_inputs.count()} input fields. Printing their outerHTML:")
                for i in range(all_inputs.count()):
                    print(all_inputs.nth(i).evaluate("el => el.outerHTML"))
                raise Exception("Could not find title input field")

            title_input.fill(title)

            print("💰 Filling Price...")

            # Find all text inputs again
            text_inputs = page.locator("input[type='text']")
            price_input = None
            title_filled = False

            for i in range(text_inputs.count()):
                el = text_inputs.nth(i)
                if el.is_visible():
                    # If this is the title input, mark as found
                    if not title_filled and el.input_value() == title:
                        title_filled = True
                        continue
                    # The next visible, empty input after title is likely the price
                    if title_filled and el.input_value() == "":
                        price_input = el
                        break

            if not price_input:
                print(
                    "Could not find price input. Printing all text input values for debug:")
                for i in range(text_inputs.count()):
                    el = text_inputs.nth(i)
                    print(
                        f"Input {i}: value='{el.input_value()}', visible={el.is_visible()}")
                raise Exception("Could not find price input field")

            price_input.fill(str(price))
            # page.locator("text=Category").first.wait_for(
            # state="visible", timeout=10000)

            print("📂 Selecting Category...")
            category_elements = page.locator("text=Category")
            for i in range(category_elements.count()):
                el = category_elements.nth(i)
                if el.is_visible():
                    el.scroll_into_view_if_needed()
                    el.click(force=True)
                    break

            page.wait_for_timeout(1000)

            # Click the exact "Furniture" option
            furniture_option = page.locator("text=Furniture")
            if furniture_option.first.is_visible():
                furniture_option.first.scroll_into_view_if_needed()
                furniture_option.first.click(force=True)
                print("✅ Selected Category: Furniture")
            else:
                print("❌ Could not find Furniture category.")

            print("🔧 Selecting Condition...")
            condition_elements = page.locator("text=Condition")
            for i in range(condition_elements.count()):
                el = condition_elements.nth(i)
                if el.is_visible():
                    el.scroll_into_view_if_needed()
                    el.click(force=True)
                    break

            page.wait_for_timeout(1000)

            # Click the exact "New" condition
            new_option = page.locator("text=New")
            if new_option.first.is_visible():
                new_option.first.scroll_into_view_if_needed()
                new_option.first.click(force=True)
                print("✅ Selected Condition: New")
            else:
                print("❌ Could not find New condition.")

            print("🧾 Filling Description...")
            try:
                # Try by accessible name
                description_area = page.get_by_role(
                    "textbox", name="Description")
                description_area.fill(description)
            except Exception:
                # Fallback: use the first visible textarea
                textareas = page.locator("textarea")
                for i in range(textareas.count()):
                    el = textareas.nth(i)
                    if el.is_visible():
                        el.fill(description)
                        break

            print("📦 Setting Availability: In Stock...")

            availability_elements = page.locator("text=List as in Stock")
            for i in range(availability_elements.count()):
                el = availability_elements.nth(i)
                if el.is_visible():
                    el.scroll_into_view_if_needed()
                    el.click(force=True)
                    break
            page.wait_for_timeout(1000)
            page.keyboard.press("Home")  # Go to top of availability list
            page.keyboard.press("ArrowDown")  # Navigate to "In Stock"
            page.keyboard.press("Enter")

            print("📍 Skipping location (using proxy/VPN for region)...")

            print("📤 Publishing...")
            page.click("text='Next'")
            page.click("text='Publish'")

            print("✅ Posted successfully!")

        except Exception as e:
            print("❌ Something went wrong while trying to fill the form.")
            page.screenshot(path="error_screenshot.png")
            print("📷 Screenshot saved as error_screenshot.png")
            raise e

        finally:
            context.close()
            browser.close()
