from django.contrib import admin
from .models import SerialKiller, Suggestion, Modification


@admin.register(SerialKiller)
class SerialKillerAdmin(admin.ModelAdmin):
    """Admin interface for Serial Killers."""
    
    list_display = ('common_name', 'full_name', 'gender', 'proven_victims', 'status', 'years_active')
    list_filter = ('gender', 'status', 'birth_country')
    search_fields = ('common_name', 'full_name', 'aliases')
    ordering = ('common_name',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('common_name', 'full_name', 'aliases', 'date_of_birth', 'birth_country', 'gender')
        }),
        ('Crime Details', {
            'fields': ('proven_victims', 'possible_victims', 'years_active', 'active_countries', 'modus_operandi')
        }),
        ('Legal Status', {
            'fields': ('capture_date', 'sentence', 'death_date', 'manner_of_death', 'status')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_fieldsets(self, request, obj=None):
        """Add timestamps to fieldsets if object exists."""
        fieldsets = super().get_fieldsets(request, obj)
        if obj:  # Editing an existing object
            fieldsets = fieldsets + (
                ('Timestamps', {
                    'fields': ('created_at', 'updated_at'),
                    'classes': ('collapse',)
                }),
            )
        return fieldsets


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    """Admin interface for Suggestions."""
    
    list_display = ('common_name', 'full_name', 'submission_status', 'proven_victims', 'years_active', 'created_at')
    list_filter = ('submission_status', 'gender', 'created_at')
    search_fields = ('common_name', 'full_name', 'aliases')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Submission Status', {
            'fields': ('submission_status',)
        }),
        ('Personal Information', {
            'fields': ('common_name', 'full_name', 'aliases', 'date_of_birth', 'birth_country', 'gender')
        }),
        ('Crime Details', {
            'fields': ('proven_victims', 'possible_victims', 'years_active', 'active_countries', 'modus_operandi')
        }),
        ('Legal Status', {
            'fields': ('capture_date', 'sentence', 'death_date', 'manner_of_death', 'status')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['mark_in_progress', 'mark_finished']
    
    @admin.action(description='Mark selected suggestions as In Progress')
    def mark_in_progress(self, request, queryset):
        updated = queryset.update(submission_status='in_progress')
        self.message_user(request, f'{updated} suggestion(s) marked as in progress.')
    
    @admin.action(description='Mark selected suggestions as Finished')
    def mark_finished(self, request, queryset):
        updated = queryset.update(submission_status='finished')
        self.message_user(request, f'{updated} suggestion(s) marked as finished.')
    
    def get_fieldsets(self, request, obj=None):
        """Add timestamps to fieldsets if object exists."""
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            fieldsets = fieldsets + (
                ('Timestamps', {
                    'fields': ('created_at', 'updated_at'),
                    'classes': ('collapse',)
                }),
            )
        return fieldsets


@admin.register(Modification)
class ModificationAdmin(admin.ModelAdmin):
    """Admin interface for Modifications."""
    
    list_display = ('get_killer_name', 'get_suggestion_preview', 'submission_status', 'created_at')
    list_filter = ('submission_status', 'created_at')
    search_fields = ('killer__common_name', 'suggestion_text')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Submission Status', {
            'fields': ('submission_status',)
        }),
        ('Modification Details', {
            'fields': ('killer', 'suggestion_text')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['mark_in_progress', 'mark_finished']
    
    @admin.display(description='Serial Killer', ordering='killer__common_name')
    def get_killer_name(self, obj):
        return obj.killer.common_name
    
    @admin.display(description='Suggestion Preview')
    def get_suggestion_preview(self, obj):
        """Show first 100 characters of suggestion."""
        if len(obj.suggestion_text) > 100:
            return f"{obj.suggestion_text[:100]}..."
        return obj.suggestion_text
    
    @admin.action(description='Mark selected modifications as In Progress')
    def mark_in_progress(self, request, queryset):
        updated = queryset.update(submission_status='in_progress')
        self.message_user(request, f'{updated} modification(s) marked as in progress.')
    
    @admin.action(description='Mark selected modifications as Finished')
    def mark_finished(self, request, queryset):
        updated = queryset.update(submission_status='finished')
        self.message_user(request, f'{updated} modification(s) marked as finished.')
    
    def get_fieldsets(self, request, obj=None):
        """Add timestamps to fieldsets if object exists."""
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            fieldsets = fieldsets + (
                ('Timestamps', {
                    'fields': ('created_at', 'updated_at'),
                    'classes': ('collapse',)
                }),
            )
        return fieldsets
