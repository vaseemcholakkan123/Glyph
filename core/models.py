from django.db import models

# Create your models here.

COLOR_CHOICES = (
    ('white', 'White'),
    ('black', 'Black'),
    ('red', 'Red'),
    ('green', 'Green'),
    ('blue', 'Blue'),
    ('yellow', 'Yellow'),
    ('orange', 'Orange'),
    ('purple', 'Purple'),
    ('pink', 'Pink'),
    ('gray', 'Gray'),
)



class Tag(models.Model):
      name = models.CharField(max_length=100)
   
      def __str__(self):
         return self.name

class Shirt(models.Model):
      name = models.CharField(max_length=100)
      price = models.IntegerField()
      image = models.ImageField(upload_to='shirts')
      description = models.TextField()
      tag = models.ManyToManyField(Tag, blank=True)
      color = models.CharField(choices=COLOR_CHOICES, max_length=100, default='white')
      type = models.CharField(default='shirt', max_length=100)
   
      def __str__(self):
         return self.name
      

class Tshirt(models.Model):
      name = models.CharField(max_length=100)
      price = models.IntegerField()
      image = models.ImageField(upload_to='shirts')
      description = models.TextField()
      tag = models.ManyToManyField(Tag, blank=True)
      color = models.CharField(choices=COLOR_CHOICES, max_length=100, default='white')
      type = models.CharField(default='tshirt', max_length=100)

   
      def __str__(self):
         return self.name