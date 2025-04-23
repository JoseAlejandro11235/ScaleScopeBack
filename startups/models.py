from django.db import models

class Startup(models.Model):
    name = models.CharField(max_length=255)
    tagline = models.TextField()
    category = models.CharField(max_length=100)
    votes = models.IntegerField()
    growth = models.FloatField()
    logo_url = models.URLField()
    product_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

