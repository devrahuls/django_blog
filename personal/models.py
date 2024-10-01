from django.db import models

# # Create your models here.

# #It behaves like a hashmap, it is nothing but a constant that holds something of length 1, that maps to the corresponding element.
# PRIORITY = [
#     ("H", "High"),
#     ("M", "Medium"),
#     ("L", "Low"),
# ]

# #This is like a table in DB named 'Question'
# class Question(models.Model):
#     title                   = models.CharField(max_length=20)
#     question                = models.TextField(max_length=400)
#     priority                = models.CharField(max_length=1, choices=PRIORITY)

#     def __str__(self):
#         return self.title
    
#     # It changes the title of the model (both singular and plural) that used to display on the Admin.
#     class Meta:
#         verbose_name = "The Question" #For each individual row name
#         verbose_name_plural = "People Questions" #The table name