from django.db import models
from authentication.models import User

# Create your models here.


class Tag(models.Model):
    ACTIVE = 0
    INACTIVE = 1
    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
    )
    tag_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=False, null=False, unique=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)


class Snippet(models.Model):
    ACTIVE = 0
    INACTIVE = 1
    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
    )
    snippet_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    text = models.CharField(max_length=5000, null=True)
    time_stamp = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
