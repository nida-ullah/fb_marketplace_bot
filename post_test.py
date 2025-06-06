from automation.post_to_facebook import save_session, login_and_post

# Replace with your test credentials
email = "nidaullah2002@gmail.com"

title = "Test Chair for Sale it is just testing"
description = "This is a comfortable chair, like new."
price = 45.00
image_path = "media/ss.png"  # Add a test image here
location = "Toronto, Canada"

login_and_post(email, title, description,
               price, image_path, location)
