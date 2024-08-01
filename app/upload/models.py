# Import the models module from Django's database package
from django.db import models

# Define a Todo model 
class Todo(models.Model):
    # racter field for the todo text 
    text = models.CharField(max_length=200)

    # boolean field to track the todo's completion status
    complete = models.BooleanField(default=False)

    # date/time field to track when the todo was created
    at = models.DateTimeField(auto_now_add=True)

    # custom string representation of the Todo instance
    def __str__(self):
        return self.text
