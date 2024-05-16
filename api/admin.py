from django.contrib import admin
from .models import Football

# Register your models here.
class FootballAdmin(admin.ModelAdmin):
    list_display=('club_name','country_name','leage')
admin.site.register(Football,FootballAdmin)
