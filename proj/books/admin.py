from django.contrib import admin
from .models import Book, Review, Contributor

class ContributorAdmin(admin.ModelAdmin):
    list_display = ('last_names', 'first_names')
    search_fields = ('last_names__startswith', 'first_names__startswith')
    list_filter = ('last_names',)

admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Contributor, ContributorAdmin)