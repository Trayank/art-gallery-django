from django.contrib import admin
from .models import Artwork, CommissionRequest, ArtClass, ContactMessage

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'medium', 'dimensions', 'price', 'is_available', 'is_featured', 'created_at')
    list_filter = ('medium', 'is_available', 'is_featured', 'created_at')
    search_fields = ('title', 'description', 'medium')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('price', 'is_available', 'is_featured')


@admin.register(CommissionRequest)
class CommissionRequestAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'email', 'phone', 'style', 'budget', 'deadline', 'created_at')
    list_filter = ('style', 'deadline', 'created_at')
    search_fields = ('client_name', 'email', 'description')
    readonly_fields = ('created_at',)


@admin.register(ArtClass)
class ArtClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'price', 'instructor', 'seats_available', 'total_seats')
    list_filter = ('date', 'instructor')
    search_fields = ('title', 'description', 'instructor')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
