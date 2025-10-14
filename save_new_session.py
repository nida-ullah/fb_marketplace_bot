#!/usr/bin/env python
"""
Quick script to save Facebook session only.
Usage: python save_new_session.py
"""
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

from automation.post_to_facebook import save_session


def main():
    print("\n" + "="*60)
    print("💾 Save Facebook Session")
    print("="*60)
    
    email = input("\n📧 Enter Facebook account email: ").strip()
    
    if not email:
        print("❌ Email cannot be empty!")
        return
    
    session_file = f"sessions/{email.replace('@', '_').replace('.', '_')}.json"
    
    if os.path.exists(session_file):
        print(f"\n⚠️  Session already exists: {session_file}")
        overwrite = input("Overwrite existing session? (yes/no): ").strip().lower()
        if overwrite not in ['yes', 'y']:
            print("✅ Keeping existing session")
            return
    
    print("\n🌐 A browser window will open.")
    print("👉 Please log in to Facebook manually.")
    print("⏳ You have 60 seconds to complete the login.\n")
    
    input("Press Enter when ready to start...")
    
    try:
        save_session(email)
        print("\n✅ Success! Session saved.")
        print(f"📁 Session file: {session_file}")
        print("\n💡 Next steps:")
        print("   1. Add this account to Django admin if not already added")
        print("   2. Create a post for this account")
        print("   3. Run: python manage.py post_to_marketplace")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
