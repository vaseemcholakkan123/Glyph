from django.contrib import admin
from .models import Shirt,Tshirt,Tag

# Register your models here.

class ShirtAdmin(admin.ModelAdmin):
    readonly_fields = ['type']

admin.site.register(Shirt , ShirtAdmin)
admin.site.register(Tag)
admin.site.register(Tshirt, ShirtAdmin)
