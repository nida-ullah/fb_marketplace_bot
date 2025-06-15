from postings.models import MarketplacePost
from .post_to_facebook import login_and_post


def auto_post():
    posts = MarketplacePost.objects.filter(posted=False)
    for post in posts:
        account = post.account
        login_and_post(account.email, account.password, post.title,
                       post.description, post.price, post.image.path, post.location)
        post.posted = True
        post.save()
