from django.contrib import admin
from .models import Trip, Photo, Place

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'city', 'country', 'total_cost', 'visibility', 'created_at')
    list_filter = ('visibility', 'country', 'city', 'created_at')
    search_fields = ('title', 'description', 'city', 'country', 'user__username')
    inlines = [PhotoInline]

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('trip', 'caption', 'uploaded_at')

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind')
    list_filter = ('kind',)
    search_fields = ('name',)
