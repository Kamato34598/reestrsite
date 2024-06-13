from django.contrib import admin
from .models import Cities, Regions

@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', )
    autocomplete_fields = ['region']
    search_fields = ('name', 'region__name', )

# @admin.register(Districts)
# class DistrictsAdmin(admin.ModelAdmin):
#     list_display = ('custom_name', 'region')
#     def custom_name(self, obj):
#         return obj.__str__()
#     list_display_links = ('custom_name',)
#     ordering = ('region__name', 'name')
#     autocomplete_fields = ['region']
#     search_fields = ('name', 'region__name', )

@admin.register(Regions)
class RegionsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
