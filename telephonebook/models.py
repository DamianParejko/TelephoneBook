from django.db import models

# Create your models here.
class Person(models.Model):

    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)

    def get_absolute_url(self):
        return "/%s/" % (self.id)

class Info(models.Model):
    person = models.ForeignKey(Person, editable=False, max_length=50, on_delete=models.CASCADE, related_name='info')
    number = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    def get_absolute_url(self):
        return "/%s/" % (self.id)