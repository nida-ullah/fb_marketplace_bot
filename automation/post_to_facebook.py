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


def login_and_post(email, title, description, price, image_path, category=None, condition='new', availability='in_stock', public_meetup=False, door_pickup=False, door_dropoff=False, brand='', color='', sku='', tags=''):
    session_file = f"sessions/{email.replace('@', '_').replace('.', '_')}.json"
    if not os.path.exists(session_file):
        raise Exception(f"❌ Session not found. Run save_session('{email}') first.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=session_file)
        page = context.new_page()

        print("🌐 Opening Marketplace listing page...")
        page.goto("https://www.facebook.com/marketplace/create/item", timeout=60000)

        try:
            print("📸 Uploading image first...")
            image_input = page.locator("input[type='file'][accept*='image']")
            image_input.set_input_files(image_path)
            page.wait_for_timeout(2000)

            print("📝 Filling Title...")
            text_inputs = page.locator("input[type='text']")
            title_input = None

            for i in range(text_inputs.count()):
                el = text_inputs.nth(i)
                if el.is_visible() and el.input_value() == "":
                    box = el.bounding_box()
                    if box and box['y'] > 100:
                        title_input = el
                        break

            if not title_input:
                raise Exception("Could not find title input field")

            title_input.fill(title)
            page.wait_for_timeout(10000)  # Wait 10 seconds for Facebook to process the title

            print("💰 Filling Price...")
            text_inputs = page.locator("input[type='text']")
            price_input = None
            title_filled = False

            for i in range(text_inputs.count()):
                el = text_inputs.nth(i)
                if el.is_visible():
                    if not title_filled and el.input_value() == title:
                        title_filled = True
                        continue
                    if title_filled and el.input_value() == "":
                        price_input = el
                        break

            if not price_input:
                raise Exception("Could not find price input field")

            price_input.fill(str(price))
            page.wait_for_timeout(5000)  # Wait 5 seconds for Facebook to process the price

            # Only try to select category if one was specified
            if category:
                print("📂 Selecting Category...")
                category_elements = page.locator("text=Category")
                category_clicked = False
                for i in range(category_elements.count()):
                    el = category_elements.nth(i)
                    if el.is_visible():
                        el.scroll_into_view_if_needed()
                        el.click(force=True)
                        category_clicked = True
                        break
                
                if category_clicked:
                    page.wait_for_timeout(2000)
                    
                    # Get the main category from the category code
                    main_category = category.split('_')[0].title()
                    subcategory = ' '.join(category.split('_')[1:]).title()
                    
                    # First select the main category
                    max_attempts = 20
                    found_main = False
                    for _ in range(max_attempts):
                        page.keyboard.press("ArrowDown")
                        page.wait_for_timeout(500)
                        selected_text = page.evaluate("() => document.activeElement.textContent")
                        if main_category in selected_text:
                            page.keyboard.press("Enter")
                            found_main = True
                            break
                    
                    if found_main:
                        page.wait_for_timeout(2000)
                        # Now select the subcategory
                        for _ in range(max_attempts):
                            page.keyboard.press("ArrowDown")
                            page.wait_for_timeout(500)
                            selected_text = page.evaluate("() => document.activeElement.textContent")
                            if subcategory in selected_text:
                                page.keyboard.press("Enter")
                                break
                    else:
                        print(f"Warning: Could not find main category {main_category}")
            else:
                print("ℹ️ No category specified - letting Facebook auto-detect based on title and description")
                page.wait_for_timeout(5000)  # Wait for auto-detection

            print("🔧 Selecting Condition...")
            condition_elements = page.locator("text=Condition")
            condition_found = False
            for i in range(condition_elements.count()):
                el = condition_elements.nth(i)
                if el.is_visible():
                    el.scroll_into_view_if_needed()
                    el.click(force=True)
                    condition_found = True
                    break
            
            if not condition_found:
                print("Warning: Could not find condition selector")
            else:
                page.wait_for_timeout(2000)
                
                # Map our condition values to Facebook's exact text
                condition_map = {
                    'new': 'New',
                    'used_like_new': 'Used - Like New',
                    'used_good': 'Used - Good',
                    'used_fair': 'Used - Fair'
                }
                
                # Select the appropriate condition
                condition_text = condition_map.get(condition, '')
                if condition_text:
                    for _ in range(10):  # Increased attempts to find condition
                        page.keyboard.press("ArrowDown")
                        page.wait_for_timeout(500)
                        selected_text = page.evaluate("() => document.activeElement.textContent")
                        if condition_text in selected_text:
                            page.keyboard.press("Enter")
                            break

            print("🧾 Filling Description...")
            try:
                description_area = page.get_by_role("textbox", name="Description")
                # Enhanced description with additional details
                enhanced_description = f"{description}\n\n"
                if brand:
                    enhanced_description += f"Brand: {brand}\n"
                if color:
                    enhanced_description += f"Color: {color}\n"
                if sku:
                    enhanced_description += f"SKU: {sku}\n"
                if tags:
                    enhanced_description += f"Tags: {tags}\n"
                
                description_area.fill(enhanced_description)
                page.wait_for_timeout(2000)  # Wait for Facebook to process the description
            except Exception:
                textareas = page.locator("textarea")
                for i in range(textareas.count()):
                    el = textareas.nth(i)
                    if el.is_visible():
                        el.fill(enhanced_description)
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
            
            # Select the appropriate availability option
            if availability == 'in_stock':
                page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            print("☑️ Selecting Meetup Preferences...")
            # Wait for meetup preferences to be visible
            page.wait_for_timeout(2000)
            
            # Select each enabled meetup preference
            if public_meetup:
                meetup_element = page.locator("text=Public Meetup").first
                if meetup_element.is_visible():
                    meetup_element.click(force=True)
                    page.wait_for_timeout(1000)
                    # Verify selection
                    if not meetup_element.is_checked():
                        meetup_element.click(force=True)
                        page.wait_for_timeout(1000)
            
            if door_pickup:
                meetup_element = page.locator("text=Door Pickup").first
                if meetup_element.is_visible():
                    meetup_element.click(force=True)
                    page.wait_for_timeout(1000)
                    # Verify selection
                    if not meetup_element.is_checked():
                        meetup_element.click(force=True)
                        page.wait_for_timeout(1000)
            
            if door_dropoff:
                meetup_element = page.locator("text=Door Drop Off").first
                if meetup_element.is_visible():
                    meetup_element.click(force=True)
                    page.wait_for_timeout(1000)
                    # Verify selection
                    if not meetup_element.is_checked():
                        meetup_element.click(force=True)
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
