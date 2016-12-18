from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Sum
from django.core.urlresolvers import reverse
import datetime


class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatars')
    info = models.TextField()