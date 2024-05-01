from django.contrib import admin
from .models import Shirt,Tshirt,Tag

# Register your models here.

admin.site.register(Shirt)
admin.site.register(Tag)
admin.site.register(Tshirt)
