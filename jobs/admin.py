from django.contrib import admin

from jobs.models import Job, LogMessage, Result


# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass


@admin.register(LogMessage)
class LogAdmin(admin.ModelAdmin):
    pass


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    pass
