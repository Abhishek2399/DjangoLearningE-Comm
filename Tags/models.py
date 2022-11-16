from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# following tag class should be generic i.e. it should be reuseable in other projects
# hence, that means we want to apply tag to any object in the project in this case it is a Product object from the Store app
# but the object will change from App to App, it can be a song for music app or a video from video streaming app
# inorder to make a generic object we already have one installed app known as the contenttype



# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    # what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE) # tag we are applying
    # in order to identify any object we require the type of the object and the ID of that object
    # ContentType is a model that represents obejct in the relation ship
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # here we have to import the Product class from the store app but then it wont be generic and will be restricted to single app
    object_id = models.PositiveIntegerField() # here we are assume the primary key is an integer
    content_object = GenericForeignKey() # this is the actual object that we will get when we query
    

