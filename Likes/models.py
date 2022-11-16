from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class LikedItem(models.Model):
    # which use has liked which item
    user = models.ForeignKey(User, on_delete=models.CASCADE) # user that has liked an item
    content = models.ForeignKey(ContentType, on_delete=models.CASCADE) # what item the user has liked
    content_id = models.PositiveIntegerField() # id of the liked item
    content_obj = GenericForeignKey() # liked item itself as an object
    



