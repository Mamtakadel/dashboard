from django.contrib import admin
from todo import models


class DashboardAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "is_done", "date"]


admin.site.register(models.Todo, DashboardAdmin)
