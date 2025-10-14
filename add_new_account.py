#!/usr/bin/env python
"""
Script to save a new Facebook account session and test posting.
Usage: python add_new_account.py
"""
from django.utils import timezone
from postings.models import MarketplacePost
from accounts.models import FacebookAccount
from automation.post_to_facebook import save_session, login_and_post
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot_core.settings')
django.setup()


def main():
    print("\n" + "="*60)
    print("📱 Facebook Account & Session Manager")
    print("="*60)

    # Ask for email
    email = input("\n📧 Enter the Facebook account email: ").strip()

    if not email:
        print("❌ Email cannot be empty!")
        return

    # Check if session already exists
    session_file = f"sessions/{email.replace('@', '_').replace('.', '_')}.json"
    session_exists = os.path.exists(session_file)

    if session_exists:
        print(f"\n⚠️  Session already exists for {email}")
        overwrite = input(
            "Do you want to re-save the session? (yes/no): ").strip().lower()
        if overwrite not in ['yes', 'y']:
            print("✅ Using existing session")
        else:
            print(f"\n🔄 Re-saving session for {email}...")
            save_session(email)
    else:
        print(f"\n💾 Saving new session for {email}...")
        print("🌐 A browser window will open. Please log in to Facebook.")
        save_session(email)

    # Check if account exists in database
    try:
        fb_account = FacebookAccount.objects.get(email=email)
        print(f"\n✅ Account found in database: {fb_account.email}")
    except FacebookAccount.DoesNotExist:
        print(f"\n⚠️  Account not found in database")
        create_account = input(
            f"Do you want to create account '{email}' in database? (yes/no): ").strip().lower()

        if create_account in ['yes', 'y']:
            password = input(
                "Enter password (for reference only): ").strip() or "password123"
            try:
                fb_account = FacebookAccount.objects.create(
                    email=email,
                    password=password  # Note: Store securely in production
                )
                print(f"✅ Account created: {fb_account.email}")
            except Exception as e:
                print(f"❌ Error creating account: {e}")
                return
        else:
            print("❌ Cannot proceed without database account")
            return

    # Ask if user wants to test posting
    print("\n" + "="*60)
    test_post = input(
        "\n🧪 Do you want to test posting with this account? (yes/no): ").strip().lower()

    if test_post not in ['yes', 'y']:
        print("\n✅ Done! Session saved successfully.")
        print(f"Session file: {session_file}")
        return

    # Create a test post
    print("\n📝 Creating a test post...")
    print("="*60)

    title = input("Enter post title (or press Enter for default): ").strip()
    if not title:
        title = "Test Product - Office Chair"

    description = input(
        "Enter description (or press Enter for default): ").strip()
    if not description:
        description = "This is a test posting to verify the Facebook Marketplace automation is working correctly. High-quality office chair in excellent condition."

    price = input("Enter price (or press Enter for default 100): ").strip()
    if not price:
        price = "100"

    try:
        price = float(price)
    except ValueError:
        print("❌ Invalid price, using default: 100")
        price = 100.0

    # Ask for image
    print("\n📸 Image options:")
    print("1. Use existing image from media/posts/")
    print("2. Enter custom image path")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        # List available images
        posts_dir = "media/posts"
        if os.path.exists(posts_dir):
            images = [f for f in os.listdir(posts_dir) if f.lower().endswith(
                ('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
            if images:
                print("\nAvailable images:")
                for i, img in enumerate(images, 1):
                    print(f"  {i}. {img}")
                img_choice = input(f"Select image (1-{len(images)}): ").strip()
                try:
                    img_idx = int(img_choice) - 1
                    if 0 <= img_idx < len(images):
                        image_path = os.path.abspath(
                            os.path.join(posts_dir, images[img_idx]))
                    else:
                        print("❌ Invalid choice, using first image")
                        image_path = os.path.abspath(
                            os.path.join(posts_dir, images[0]))
                except ValueError:
                    print("❌ Invalid choice, using first image")
                    image_path = os.path.abspath(
                        os.path.join(posts_dir, images[0]))
            else:
                print("❌ No images found in media/posts/")
                return
        else:
            print("❌ media/posts/ directory not found")
            return
    else:
        image_path = input("Enter image path: ").strip()
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return
        image_path = os.path.abspath(image_path)

    print(f"\n📋 Test Post Details:")
    print(f"  Account: {email}")
    print(f"  Title: {title}")
    print(f"  Price: ${price}")
    print(f"  Description: {description[:50]}...")
    print(f"  Image: {image_path}")

    confirm = input(
        "\n⚠️  Proceed with test posting? (yes/no): ").strip().lower()

    if confirm not in ['yes', 'y']:
        print("❌ Test cancelled")
        return

    # Perform the test post
    print("\n🚀 Starting test post...")
    print("="*60)

    try:
        login_and_post(
            email=email,
            title=title,
            description=description,
            price=price,
            image_path=image_path
        )
        print("\n" + "="*60)
        print("✅ Test post completed successfully!")
        print("="*60)

        # Ask if they want to save this as a scheduled post
        save_to_db = input(
            "\n💾 Save this as a scheduled post in database? (yes/no): ").strip().lower()
        if save_to_db in ['yes', 'y']:
            try:
                # Check if image is in media folder for the model
                if not image_path.startswith(os.path.abspath('media')):
                    print(
                        "⚠️  Warning: Image is outside media folder. Copy it to media/posts/ first.")
                    return

                # Create relative path from media root
                relative_path = os.path.relpath(
                    image_path, os.path.abspath('media'))

                post = MarketplacePost.objects.create(
                    account=fb_account,
                    title=title,
                    description=description,
                    price=price,
                    image=relative_path,
                    scheduled_time=timezone.now(),
                    posted=True  # Mark as posted since we just posted it
                )
                print(f"✅ Post saved to database: {post.title}")
            except Exception as e:
                print(f"❌ Error saving to database: {e}")

    except Exception as e:
        print("\n" + "="*60)
        print(f"❌ Test post failed: {e}")
        print("="*60)
        print("\n💡 Tips:")
        print("  - Check if the session is still valid")
        print("  - Try re-saving the session")
        print("  - Check error_screenshot.png if it was generated")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(0)
