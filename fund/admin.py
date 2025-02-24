from django.contrib import admin

# Register your models here.
from .models import Comment,Category,Rate

admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Rate)

