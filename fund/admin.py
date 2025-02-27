from django.contrib import admin

# Register your models here.

from .models import Comment,Category,Rate,Reply,User,Report,Project,Tag



admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Rate)
admin.site.register(Reply)
admin.site.register(User)
admin.site.register(Report)
admin.site.register(Project)
admin.site.register(Tag)


