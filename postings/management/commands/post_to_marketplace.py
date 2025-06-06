from django.core.management.base import BaseCommand
from postings.models import MarketplacePost
from automation.post_to_facebook import login_and_post
from django.utils import timezone
from django.db.models import QuerySet, Manager
import os


class Command(BaseCommand):
    help = 'Posts scheduled marketplace listings to Facebook'

    def handle(self, *args, **options):
        print("Checking for posts to publish...")

        # Get all posts that are scheduled for now or earlier and haven't been posted
        posts: QuerySet[MarketplacePost] = MarketplacePost.objects.filter(  # type: ignore[attr-defined]
            scheduled_time__lte=timezone.now(),
            posted=False
        )

        print(f"Found {posts.count()} posts to publish")

        if posts.count() == 0:
            print("No posts found to publish. Make sure you have:")
            print("1. Created posts in the admin interface")
            print("2. Set scheduled_time to a past or current time")
            print("3. Set posted=False")
            return

        for post in posts:
            try:
                print(f"\nProcessing post: {post.title}")
                # Get the absolute path of the image
                image_path = os.path.abspath(post.image.path)
                print(f"Image path: {image_path}")

                # Post to Facebook
                login_and_post(
                    email=post.account.email,
                    title=post.title,
                    description=post.description,
                    price=float(post.price),
                    image_path=image_path,
                    location=post.location
                )

                # Mark as posted
                post.posted = True
                post.save()

                print(
                    f'Successfully posted "{post.title}" to {post.account.email}')

            except Exception as e:
                print(
                    f'Failed to post "{post.title}" to {post.account.email}: {str(e)}')
                print(f"Error details: {str(e)}")
