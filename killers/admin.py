from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django import forms
from django.db.models import Q
from .models import SerialKiller, Suggestion, Modification


@admin.register(SerialKiller)
class SerialKillerAdmin(admin.ModelAdmin):
    """Admin interface for Serial Killers."""
    
    list_display = ('common_name', 'full_name', 'gender', 'proven_victims', 'status', 'years_active', 'assigned_to')
    list_filter = ('gender', 'status', 'birth_country', 'assigned_to')
    search_fields = ('common_name', 'full_name', 'aliases')
    ordering = ('common_name',)
    
    def get_queryset(self, request):
        """Filter queryset based on user permissions."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Staff users see killers assigned to them OR killers with modifications assigned to them
        return qs.filter(Q(assigned_to=request.user) | Q(modifications__assigned_to=request.user)).distinct()
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Customize form fields to make certain TextFields single-line."""
        if db_field.name in ['aliases', 'active_countries', 'modus_operandi', 'sentence']:
            kwargs['widget'] = forms.TextInput(attrs={'size': '80', 'style': 'width: 100%;'})
            return db_field.formfield(**kwargs)
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
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
        ('Assignment', {
            'fields': ('assigned_to',),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_readonly_fields(self, request, obj=None):
        """Make assigned_to read-only for non-superusers."""
        readonly = list(self.readonly_fields)
        if not request.user.is_superuser:
            readonly.append('assigned_to')
        return readonly
    
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
    
    list_display = ('common_name', 'full_name', 'submission_status', 'proven_victims', 'years_active', 'assigned_to', 'created_at')
    list_filter = ('submission_status', 'gender', 'assigned_to', 'created_at')
    search_fields = ('common_name', 'full_name', 'aliases')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        """Filter queryset based on user permissions."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Staff users only see suggestions assigned to them
        return qs.filter(assigned_to=request.user)
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Customize form fields to make certain TextFields single-line."""
        if db_field.name in ['aliases', 'active_countries', 'modus_operandi', 'sentence']:
            kwargs['widget'] = forms.TextInput(attrs={'size': '80', 'style': 'width: 100%;'})
            return db_field.formfield(**kwargs)
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    fieldsets = (
        ('Submission Status', {
            'fields': ('submission_status', 'assigned_to')
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
    
    actions = ['mark_in_progress', 'mark_finished', 'approve_and_create_killer']
    
    def get_readonly_fields(self, request, obj=None):
        """Make assigned_to read-only for non-superusers."""
        readonly = list(self.readonly_fields)
        if not request.user.is_superuser:
            readonly.append('assigned_to')
        return readonly
    
    @admin.action(description='Approve and Create Serial Killer')
    def approve_and_create_killer(self, request, queryset):
        """Convert approved suggestions into SerialKiller records."""
        created_count = 0
        for suggestion in queryset:
            # Create a new SerialKiller from the suggestion
            killer = SerialKiller.objects.create(
                common_name=suggestion.common_name,
                full_name=suggestion.full_name,
                aliases=suggestion.aliases,
                date_of_birth=suggestion.date_of_birth,
                birth_country=suggestion.birth_country,
                gender=suggestion.gender,
                proven_victims=suggestion.proven_victims,
                possible_victims=suggestion.possible_victims,
                years_active=suggestion.years_active,
                active_countries=suggestion.active_countries,
                modus_operandi=suggestion.modus_operandi,
                capture_date=suggestion.capture_date,
                sentence=suggestion.sentence,
                death_date=suggestion.death_date,
                manner_of_death=suggestion.manner_of_death,
                status=suggestion.status,
                notes=suggestion.notes,
                assigned_to=request.user  # Assign to the user who approved it
            )
            # Mark suggestion as finished
            suggestion.submission_status = 'finished'
            suggestion.save()
            created_count += 1
        
        self.message_user(request, f'{created_count} suggestion(s) approved and added to database.')
    
    actions = ['mark_in_progress', 'mark_finished', 'approve_and_create_killer']
    
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
    
    list_display = ('get_killer_name', 'get_suggestion_preview', 'submission_status', 'assigned_to', 'created_at')
    list_filter = ('submission_status', 'assigned_to', 'created_at')
    search_fields = ('killer__common_name', 'suggestion_text')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        """Filter queryset based on user permissions."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Staff users only see modifications assigned to them
        return qs.filter(assigned_to=request.user)
    
    fieldsets = (
        ('Submission Status', {
            'fields': ('submission_status', 'assigned_to')
        }),
        ('Modification Details', {
            'fields': ('killer', 'suggestion_text')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['mark_in_progress', 'mark_finished']
    
    def get_readonly_fields(self, request, obj=None):
        """Make assigned_to read-only for non-superusers."""
        readonly = list(self.readonly_fields)
        if not request.user.is_superuser:
            readonly.append('assigned_to')
        return readonly
    
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


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """Admin interface for viewing system logs."""
    
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('user', 'action_flag', 'content_type', 'action_time')
    search_fields = ('object_repr', 'change_message')
    date_hierarchy = 'action_time'
    ordering = ('-action_time',)
    
    def has_add_permission(self, request):
        return False
        
    def has_change_permission(self, request, obj=None):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False
