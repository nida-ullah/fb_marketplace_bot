#!/usr/bin/env python
"""
Test script to diagnose Facebook Marketplace posting issues.
This script will open the marketplace form and pause, allowing you to inspect it.

Usage: python test_marketplace_form.py
"""
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

from playwright.sync_api import sync_playwright
import time


def test_marketplace_form(email):
    """Test the marketplace form and pause for inspection"""
    session_file = f"sessions/{email.replace('@', '_').replace('.', '_')}.json"
    
    if not os.path.exists(session_file):
        print(f"❌ Session not found: {session_file}")
        print(f"💡 Run: python save_new_session.py")
        return
    
    print(f"✅ Found session file: {session_file}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=session_file)
        page = context.new_page()
        
        print("\n🌐 Opening Marketplace listing page...")
        page.goto("https://www.facebook.com/marketplace/create/item", timeout=60000)
        
        print("\n⏸️  PAUSED FOR INSPECTION")
        print("="*60)
        print("The browser will stay open so you can:")
        print("  1. Manually fill the form")
        print("  2. Check if 'Next' button exists")
        print("  3. Check the exact text on Publish button")
        print("  4. Check for any validation errors")
        print("  5. Check account restrictions/warnings")
        print("\n💡 Take note of:")
        print("  - Does the form have multiple pages or just one?")
        print("  - What is the exact text on the publish button?")
        print("  - Are there any required fields not being filled?")
        print("  - Does the account have marketplace access?")
        print("="*60)
        
        input("\nPress Enter when you're done inspecting...")
        
        # Take screenshot of current state
        screenshot_path = "test_inspection.png"
        page.screenshot(path=screenshot_path)
        print(f"\n📷 Screenshot saved: {screenshot_path}")
        
        # Print all buttons
        print("\n🔍 All visible buttons on page:")
        buttons = page.locator("button").all()
        for i, btn in enumerate(buttons):
            try:
                if btn.is_visible():
                    text = btn.inner_text()
                    aria_label = btn.get_attribute("aria-label") or "N/A"
                    print(f"  {i+1}. Text: '{text}' | Aria-label: '{aria_label}'")
            except Exception as e:
                print(f"  {i+1}. Error reading button: {e}")
        
        # Check for errors
        print("\n🔍 Checking for error messages:")
        errors = page.locator("[role='alert'], .error, [aria-invalid='true']").all()
        error_found = False
        for i, err in enumerate(errors):
            try:
                if err.is_visible():
                    text = err.inner_text()
                    print(f"  Error {i+1}: {text}")
                    error_found = True
            except Exception:
                pass
        
        if not error_found:
            print("  ✅ No errors found")
        
        print(f"\n🔗 Current URL: {page.url}")
        
        context.close()
        browser.close()
        
        print("\n✅ Test complete!")
        print("💡 Use the information above to update the script if needed.")


def main():
    print("\n" + "="*60)
    print("🧪 Marketplace Form Testing Tool")
    print("="*60)
    
    email = input("\n📧 Enter Facebook account email to test: ").strip()
    
    if not email:
        print("❌ Email cannot be empty!")
        return
    
    try:
        test_marketplace_form(email)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
