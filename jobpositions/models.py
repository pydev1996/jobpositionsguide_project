from django.db import models

class JobPosition(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.TextField()

    def __str__(self):
        return self.title


