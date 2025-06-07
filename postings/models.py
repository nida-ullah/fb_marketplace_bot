from django.db import models
from accounts.models import FacebookAccount


class MarketplacePost(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used_like_new', 'Used - Like New'),
        ('used_good', 'Used - Good'),
        ('used_fair', 'Used - Fair'),
    ]

    AVAILABILITY_CHOICES = [
        ('single_item', 'List as Single Item'),
        ('in_stock', 'List as In Stock'),
    ]

    MEETUP_CHOICES = [
        ('public_meetup', 'Public Meetup'),
        ('door_pickup', 'Door Pickup'),
        ('door_dropoff', 'Door Drop Off'),
    ]

    CATEGORY_CHOICES = [
        # Home & Garden
        ('home_garden_tools', 'Home & Garden - Tools'),
        ('home_garden_furniture', 'Home & Garden - Furniture'),
        ('home_garden_household', 'Home & Garden - Household'),
        ('home_garden_garden', 'Home & Garden - Garden'),
        ('home_garden_appliance', 'Home & Garden - Appliance'),
        
        # Entertainment
        ('entertainment_video_games', 'Entertainment - Video Games'),
        ('entertainment_books', 'Entertainment - Books'),
        ('entertainment_movies_music', 'Entertainment - Movies & Music'),
        
        # Clothing and Accessories
        ('clothing_bags_luggage', 'Clothing and Accessories - Bags & Luggage'),
        ('clothing_womens', 'Clothing and Accessories - Women\'s Clothing & Shoes'),
        ('clothing_mens', 'Clothing and Accessories - Men\'s Clothing & Shoes'),
        ('clothing_jewelry', 'Clothing and Accessories - Jewelry & Accessories'),
        
        # Family
        ('family_toys_games', 'Family - Toys & Games'),
        ('family_baby_kids', 'Family - Baby & Kids'),
        ('family_pet_supplies', 'Family - Pet Supplies'),
        ('family_health_beauty', 'Family - Health & Beauty'),
        
        # Electronics
        ('electronics_mobile', 'Electronics - Mobile Phones'),
        ('electronics_computers', 'Electronics - Electronics & Computers'),
        
        # Hobbies
        ('hobbies_sports', 'Hobbies - Sports and Outdoors'),
        ('hobbies_musical', 'Hobbies - Musical Instruments'),
        ('hobbies_arts', 'Hobbies - Arts & Crafts'),
        ('hobbies_antiques', 'Hobbies - Antiques & Collectables'),
        ('hobbies_auto_parts', 'Hobbies - Auto Parts'),
        ('hobbies_bicycles', 'Hobbies - Bicycles'),
        
        # Classified
        ('classified_garage_sales', 'Classified - Garage Sales'),
        ('classified_miscellaneous', 'Classified - Miscellaneous'),
    ]

    account = models.ForeignKey(FacebookAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='posts/')
    scheduled_time = models.DateTimeField()
    posted = models.BooleanField(default=False)
    
    # Category and condition
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='home_garden_furniture')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='in_stock')
    
    # Meetup preferences (optional multiple choice)
    public_meetup = models.BooleanField(default=False)
    door_pickup = models.BooleanField(default=False)
    door_dropoff = models.BooleanField(default=False)
    
    # Product details (all optional)
    brand = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    sku = models.CharField(max_length=100, null=True, blank=True, help_text="Stock Keeping Unit - Optional identifier for your product")
    tags = models.CharField(max_length=255, null=True, blank=True, help_text="Comma-separated tags for better searchability")

    def __str__(self):
        return f"{self.title} - {self.account.email}"

    def get_meetup_preferences(self):
        """Returns a list of selected meetup preferences"""
        preferences = []
        if self.public_meetup:
            preferences.append('public_meetup')
        if self.door_pickup:
            preferences.append('door_pickup')
        if self.door_dropoff:
            preferences.append('door_dropoff')
        return preferences
