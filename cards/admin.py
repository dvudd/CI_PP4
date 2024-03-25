from django.contrib import admin
from .models import Subject, Deck, Card


class CardInline(admin.TabularInline):
    """
    Defines the inline admin interface for Card objects.
    This allows Cards to be edited inline within the Deck admin page.
    """
    model = Card
    extra = 1


class DeckAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for Deck objects.
    """
    inlines = [CardInline]
    list_display = ('name', 'subject', 'created_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('name', 'subject__name')


class SubjectAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for Subject objects.
    """
    list_display = ('name', 'creator', 'created_at')
    list_filter = ('creator', 'created_at')
    search_fields = ('name', 'creator__username')


class CardAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for Card objects.
    """
    list_display = ('question', 'deck', 'created_at')
    list_filter = ('deck', 'created_at')
    search_fields = ('question', 'answer', 'deck__name')


# Register models with their respective admin class.
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Deck, DeckAdmin)
admin.site.register(Card, CardAdmin)
