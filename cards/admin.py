from django.contrib import admin
from .models import Subject, Deck, Card

class CardInline(admin.TabularInline):
    model = Card
    extra = 1

class DeckAdmin(admin.ModelAdmin):
    inlines = [CardInline]
    list_display = ('name', 'subject', 'created_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('name', 'subject__name')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'created_at')
    list_filter = ('creator', 'created_at')
    search_fields = ('name', 'creator__username')

class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'deck', 'created_at')
    list_filter = ('deck', 'created_at')
    search_fields = ('question', 'answer', 'deck__name')

# Register your models here.
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Deck, DeckAdmin)
admin.site.register(Card, CardAdmin)