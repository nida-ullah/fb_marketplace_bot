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


def login_and_post(email, title, description, price, image_path, location):
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

            print("📂 Selecting Category...")
            # Find all elements with the text "Category"
            category_elements = page.locator("text=Category")
            for i in range(category_elements.count()):
                el = category_elements.nth(i)
                if el.is_visible():
                    el.scroll_into_view_if_needed()
                    el.click(force=True)
                    break
            page.wait_for_timeout(1000)
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            print("🔧 Selecting Condition...")
            condition_elements = page.locator("text=Condition")
            for i in range(condition_elements.count()):
                el = condition_elements.nth(i)
                if el.is_visible():
                    el.scroll_into_view_if_needed()
                    el.click(force=True)
                    break
            page.wait_for_timeout(1000)
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

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

            print("📦 Selecting Availability...")
            availability_elements = page.locator("text=List as in Stock")
            for i in range(availability_elements.count()):
                el = availability_elements.nth(i)
                if el.is_visible():
                    el.scroll_into_view_if_needed()
                    el.click(force=True)
                    break
            page.wait_for_timeout(1000)
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            print("📍 Filling Location...")
            location_input = page.locator("input[aria-label='Location']")
            location_input.fill("Toronto, Ontario")  # Use the correct location
            page.wait_for_timeout(2000)  # Let suggestions load

            # Try to select the first suggestion from the dropdown
            try:
                page.keyboard.press("ArrowDown")
                page.keyboard.press("Enter")
                print("Selected first location suggestion.")
            except Exception:
                print(
                    "Could not select location suggestion, please check location input.")
            page.wait_for_timeout(1000)

            print("☑️ Selecting Meetup Preference (if required)...")
            # Try to check the first visible checkbox or radio button after location
            checkboxes = page.locator(
                "input[type='checkbox'], input[type='radio']")
            checked = False
            for i in range(checkboxes.count()):
                el = checkboxes.nth(i)
                if el.is_visible() and not el.is_checked():
                    el.scroll_into_view_if_needed()
                    el.check(force=True)
                    checked = True
                    print("Checked a meetup preference option.")
                    break
            if not checked:
                print(
                    "No visible meetup preference checkbox/radio found or already checked.")
            page.wait_for_timeout(1000)

            print("📤 Publishing...")
            page.click("text='Next'")
            page.wait_for_timeout(2000)
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

# def login_and_post(email, title, description, price, image_path, location):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()

#         print("🌐 Logging into Facebook...")
#         page.goto("https://www.facebook.com/marketplace/create/item")

#         # Login (reuse cookies/session if you have it)
#         page.fill("input[name='email']", email)
#         page.fill("input[name='pass']", "your_password")  # Replace securely
#         page.click("button[name='login']")
#         page.wait_for_timeout(5000)  # Wait for login to complete

#         print("📸 Uploading image...")
#         image_input = page.locator("input[type='file']")
#         image_input.set_input_files(image_path)
#         page.wait_for_timeout(5000)  # Let FB process the image

#         print("📝 Filling title...")
#         page.locator("input[placeholder='Title']").wait_for()
#         page.fill("input[placeholder='Title']", title)

#         print("💰 Filling price...")
#         page.fill("input[placeholder='Price']", str(price))

#         print("📂 Selecting category...")
#         page.locator("text=Category").click()
#         page.keyboard.press("ArrowDown")
#         page.keyboard.press("Enter")  # Select first category

#         print("🔧 Selecting condition...")
#         page.locator("text=Condition").click()
#         page.keyboard.press("ArrowDown")
#         page.keyboard.press("Enter")  # Select first condition

#         print("🧾 Filling description...")
#         page.fill("textarea", description)

#         print("📦 Selecting availability...")
#         page.locator("text=List as in Stock").click()
#         page.keyboard.press("ArrowDown")
#         page.keyboard.press("Enter")

#         print("📍 Filling location...")
#         location_input = page.locator("input[aria-label='Location']")
#         location_input.fill(location)
#         page.wait_for_timeout(2000)
#         page.keyboard.press("ArrowDown")
#         page.keyboard.press("Enter")

#         print("📤 Publishing...")
#         page.click("text='Next'")
#         page.wait_for_timeout(2000)
#         page.click("text='Publish'")

#         print("✅ Listing posted successfully!")

#         context.close()
#         browser.close()


# def login_and_post(email, title, description, price, image_path, location):
#     session_file = f"sessions/{email.replace('@', '_').replace('.', '_')}.json"
#     if not os.path.exists(session_file):
#         raise Exception(
#             f"❌ Session not found. Run save_session('{email}') first.")

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context(storage_state=session_file)
#         page = context.new_page()

#         print("🌐 Opening Marketplace listing page...")
#         page.goto("https://www.facebook.com/marketplace/create/item",
#                   timeout=60000)

#         try:
#             # Try exact selector first
#             title_input = page.locator("input[aria-label='Title']")
#             if not title_input.is_visible():
#                 print("❗ aria-label not found, using first input fallback...")
#                 title_input = page.locator("input").first  # fallback

#             title_input.wait_for(timeout=60000)
#             title_input.fill(title)

#             # Continue filling other fields
#             page.locator("input[aria-label='Price']").fill(str(price))
#             page.locator("textarea").fill(description)
#             page.set_input_files("input[type='file']", image_path)
#             page.locator("input[aria-label='Location']").fill(location)

#             page.click("text='Next'")
#             time.sleep(3)
#             page.click("text='Publish'")
#             print("✅ Posted successfully!")

#         except Exception as e:
#             print("❌ Something went wrong while trying to fill the form.")
#             page.screenshot(path="error_screenshot.png")
#             print("📷 Screenshot saved as error_screenshot.png")
#             raise e
