from djongo import models

# Create your models here.

class Table(models.Model):
    _id = models.ObjectIdField()
    headline = models.TextField()
    article_link = models.TextField()
    date = models.TextField()
    source_site = models.TextField()
    created_at = models.TextField()

    
