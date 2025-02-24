from django.contrib import admin

# Register your models here.
from .models import Comment,Category,Rate,Reply

admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Rate)
admin.site.register(Reply)

