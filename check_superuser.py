#!/usr/bin/env python
"""
Script to check if a superuser exists, verify password, or create a new one.
Usage: python check_superuser.py
"""
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot_core.settings')
django.setup()


User = get_user_model()


def check_and_manage_superuser():
    """Check if superuser exists, verify password, or create new one."""

    # Check if any superuser exists
    superusers = User.objects.filter(is_superuser=True)

    if superusers.exists():
        print(f"\n✓ Found {superusers.count()} superuser(s):")
        for user in superusers:
            print(f"  - Username: {user.username}")
            print(f"    Email: {user.email}")
            print(f"    Active: {user.is_active}")
            print(f"    Staff: {user.is_staff}")

        # Ask to verify password
        print("\n" + "="*50)
        verify = input(
            "\nDo you want to verify a superuser password? (yes/no): ").strip().lower()

        if verify in ['yes', 'y']:
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()

            # Authenticate the user
            user = authenticate(username=username, password=password)

            if user is not None and user.is_superuser:
                print(f"\n✓ Password is correct for superuser '{username}'!")
            else:
                print(
                    f"\n✗ Authentication failed. Either the password is wrong or '{username}' is not a superuser.")

                # Option to reset password
                reset = input(
                    f"\nDo you want to reset the password for '{username}'? (yes/no): ").strip().lower()
                if reset in ['yes', 'y']:
                    try:
                        user = User.objects.get(username=username)
                        new_password = input("Enter new password: ").strip()
                        user.set_password(new_password)
                        user.save()
                        print(
                            f"\n✓ Password reset successfully for '{username}'!")
                    except User.DoesNotExist:
                        print(f"\n✗ User '{username}' does not exist.")
    else:
        print("\n✗ No superuser found in the database.")
        create = input(
            "\nDo you want to create a new superuser? (yes/no): ").strip().lower()

        if create in ['yes', 'y']:
            username = input("Enter username: ").strip()
            email = input("Enter email: ").strip()
            password = input("Enter password: ").strip()

            try:
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                print(f"\n✓ Superuser '{username}' created successfully!")
            except Exception as e:
                print(f"\n✗ Error creating superuser: {e}")


if __name__ == '__main__':
    try:
        check_and_manage_superuser()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
