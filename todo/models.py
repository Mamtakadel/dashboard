from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    is_done = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
