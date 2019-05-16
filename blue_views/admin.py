from django.contrib import admin
#마이그레이션 전에 삭제했다가 다시 살린다.
from BoulderBlueServerWebApp.blue_views.models import *

class BaseAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'mac', 'visible', 'last_seen')
    search_fields = ( 'name', 'mac', 'visible')

class ChipComandAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'command', 'get_category_name')
    readonly_fields = ('image_tag2',)

class CommandCategoryAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'index')

class ScheduledCommandAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'active', 'type', 'execution_date_or_start_date', 'get_registered_chip', 'get_command', 'retry_if_fails')
    search_fields = ( 'name', 'active', 'type')
    save_as = True
    readonly_fields = ('image_tag', 'image_tag2',)

admin.site.register(DiscoveredChip, BaseAdmin)
admin.site.register(RegisteredChip, BaseAdmin)
admin.site.register(ChipCommand, ChipComandAdmin)
admin.site.register(CommandCategory, CommandCategoryAdmin)
admin.site.register(CommandLog)
admin.site.register(ScheduledCommand, ScheduledCommandAdmin)
