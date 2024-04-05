from django.contrib import admin

# Register your models here.
from palika import models


class UserAuthAdmin(admin.ModelAdmin):
    list_display = ["id","username","password","email","firstname","lastname"]


admin.site.register(models.UserAuth, UserAuthAdmin)