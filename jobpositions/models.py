# from django.db import models

# class JobPosition(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     skills = models.TextField()

#     def __str__(self):
#         return self.title


from django.db import models

class JobPosition(models.Model):
    CATEGORY_CHOICES = [
        ('IT', 'IT'),
        ('Medical', 'Medical'),
        ('Electrical', 'Electrical'),
        ('Electronics', 'Electronics'),
        ('BPO', 'BPO'),
        ('Construction Field', 'Construction Field'),
        ('Mechanical', 'Mechanical'),
         ('Farming', 'Farming'),
         ('Sales','Sales')
        # Add more categories as needed
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.TextField()
    proceedings = models.TextField(default="")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES,default='IT')

    def __str__(self):
        return self.title

from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name


class Institutor(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)  # You may adjust the max length based on your requirements
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    repassword = models.CharField(max_length=255)

    def __str__(self):
        return self.username