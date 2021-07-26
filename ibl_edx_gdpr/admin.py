from django.contrib import admin

from completion.models import BlockCompletion


@admin.register(BlockCompletion)
class BlockCompletionAdmin(admin.ModelAdmin):
    # NOTE: context_key only in version 3+, previously course_key
    list_display = (
        'user', 'completion_context_key',
        'block_key', 'block_type', 'completion'
    )
    search_fields = ('user', 'block_key')
    list_filter = ('block_type',)
    
    def completion_context_key(self, obj):
        if hasattr(obj, "context_key"):
            return str(obj.context_key)
        elif hasattr(obj, "course_key"):
            return str(obj.course_key)
        else:
            return ""
    completion_context_key.short_description = 'Content Key'
