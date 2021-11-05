from django.contrib import admin

from project.models import Project

# Register your models here.


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    autocomplete_fields = ['members']
