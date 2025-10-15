🚀 Facebook Marketplace Automation with Django & Playwright
Automated system to post products to Facebook Marketplace using Django backend and Playwright browser automation.

📄 Features
Add and manage Facebook accounts via Django admin.

Save Facebook sessions securely (manual login required only once).

Upload and schedule Marketplace posts from Django admin.

**📦 NEW: Ultra-Simple Bulk Upload** - CSV with just 3 columns (title, description, price)!

Automatically reuse sessions to avoid repeated logins.

Supports multiple accounts (future extensions possible).

Headless or visible browser automation using Playwright.

⚙️ Requirements
Python 3.9+ (recommended)
Django (4.x or above)
Playwright
SQLite (default) or any other supported DB
Chrome/Chromium (for Playwright)

🏗️ Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/your-username/facebook-marketplace-automation.git
cd facebook-marketplace-automation

2️⃣ Create virtual environment & install requirements
python -m venv env
source env/bin/activate      # On Windows: env\Scripts\activate
pip install -r requirements.txt

3️⃣ Install Playwright browsers
playwright install

4️⃣ Set up database
python manage.py makemigrations
python manage.py migrate

5️⃣ Create superuser (to access Django admin)
python manage.py createsuperuser

6️⃣ Run the server
python manage.py runserver
Then visit: http://127.0.0.1:8000/admin/ to access admin panel.

✅ How to use
➕ Add Facebook Account
Go to Django admin > Accounts > Facebook accounts.

Add email and save.

Important: Initially, no session is saved.

💻 Save Facebook session
After adding an account:

python manage.py save_facebook_session your_email@example.com
A Playwright browser will open.
Log in manually to your Facebook account (enter 2FA if needed).
After success, session file will be saved under sessions/.
You only need to do this once per account.

📝 Add Marketplace post

**Option 1: Single Post**
Go to Postings > Marketplace posts in admin.
Add title, description, price, image, and select account.
Set scheduled_time to now or any past date to post immediately.
Save.

**Option 2: Bulk Upload (NEW!) 📦 - SUPER SIMPLE**
1. Create a CSV file with just 3 columns: `title,description,price`
2. Visit `http://localhost:8000/bulk-upload/`
3. Upload CSV - posts will be created instantly!
4. Go to Django Admin to assign accounts and add images
5. Run `python manage.py post_to_marketplace` to publish

🚀 Post to Marketplace
python manage.py post_to_marketplace
Will check for posts where posted = False and scheduled_time <= now.

Posts to Facebook Marketplace using saved session.

Updates posted = True after successful post.

💡 Folder structure
accounts/
    models.py        # Facebook account model
postings/
    models.py        # Marketplace post model
automation/
    post_to_facebook.py  # Playwright login and posting logic
sessions/
    *.json           # Saved Playwright session files
media/
    posts/           # Uploaded images

🛡️ Notes & Limitations
Sessions must be manually saved once per account.
Facebook may require manual CAPTCHA solving on first login.
Avoid using weak or fake accounts — could be flagged by Facebook.
Current implementation selects Furniture category and New condition by default.
Location selection is skipped (use VPN/proxy if targeting region).

🤝 Contributing
PRs and improvements are welcome! Please fork and submit pull requests.
