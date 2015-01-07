from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class SnippetManager(models.Manager):
    def create_snippet(self, user, title, language, source):
        snippet = self.create(user=user,
                              title=title,
                              language=language,
                              source=source)
        return snippet

class Snippet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(default='Unknown snippy', max_length=30)
    language = models.CharField(default='C', max_length=30)
    source = models.TextField()
    date = models.DateTimeField('date published', auto_now_add=True)

    objects = SnippetManager()

