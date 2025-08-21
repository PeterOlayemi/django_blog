from django.contrib import admin
from .models import *

# Register your models here.

admin.site.site_header = "InkWave Admin"
admin.site.site_title = "InkWave Admin Portal"
admin.site.index_title = "Welcome to InkWave Admin Portal"

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Comment)
