from django.contrib import admin
from badges.models import Badge, BadgeCounter, BadgeLevel

class BadgeCounterAdmin(admin.ModelAdmin):
    raw_id_fields = ("user","badge",)
    list_display = ('user', 'badge', 'count')
    #list_filter = ('is_awarded', )

class BadgeLevelInline(admin.TabularInline):
    model = BadgeLevel

class BadgeAdmin(admin.ModelAdmin):
    inlines = [
        BadgeLevelInline,
    ]
admin.site.register(Badge, BadgeAdmin)
admin.site.register(BadgeCounter, BadgeCounterAdmin)
