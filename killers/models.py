from django.db import models


class SerialKiller(models.Model):
    """Model representing a serial killer in the database."""
    
    # Personal Information
    common_name = models.CharField(max_length=255, db_index=True, help_text="Common name or nickname")
    full_name = models.CharField(max_length=255, blank=True, null=True, help_text="Full legal name")
    aliases = models.TextField(blank=True, null=True, help_text="Known aliases or other names")
    date_of_birth = models.DateField(blank=True, null=True)
    birth_country = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    
    # Crime Details
    proven_victims = models.CharField(max_length=50, blank=True, null=True, help_text="Number of proven victims (e.g., '17' or '100+')")
    possible_victims = models.CharField(max_length=50, blank=True, null=True, help_text="Possible victim count")
    years_active = models.CharField(max_length=100, blank=True, null=True, help_text="Years active (e.g., '1974-1978')")
    active_countries = models.TextField(blank=True, null=True, help_text="Countries where crimes occurred")
    modus_operandi = models.TextField(blank=True, null=True, help_text="Method of operation")
    
    # Legal Status
    capture_date = models.DateField(blank=True, null=True)
    sentence = models.TextField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    manner_of_death = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, help_text="Current status (e.g., Executed, Imprisoned)")
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    
    # Timestamps (if they exist in Supabase)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = 'Serial Killers'
        managed = True
        ordering = ['common_name']
        verbose_name = 'Serial Killer'
        verbose_name_plural = 'Serial Killers'
    
    def __str__(self):
        return self.common_name


class Suggestion(models.Model):
    """Model for user suggestions of new serial killers."""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]
    
    # Personal Information
    common_name = models.CharField(max_length=255, help_text="Common name or nickname")
    full_name = models.CharField(max_length=255, blank=True, null=True)
    aliases = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    birth_country = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    
    # Crime Details
    proven_victims = models.CharField(max_length=50, blank=True, null=True)
    possible_victims = models.CharField(max_length=50, blank=True, null=True)
    years_active = models.CharField(max_length=100, blank=True, null=True)
    active_countries = models.TextField(blank=True, null=True)
    modus_operandi = models.TextField(blank=True, null=True)
    
    # Legal Status
    capture_date = models.DateField(blank=True, null=True)
    sentence = models.TextField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    manner_of_death = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    
    # Submission tracking
    submission_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = 'Suggestions'
        managed = True
        ordering = ['-created_at']
        verbose_name = 'Suggestion'
        verbose_name_plural = 'Suggestions'
    
    def __str__(self):
        return f"{self.common_name} - {self.get_submission_status_display()}"


class Modification(models.Model):
    """Model for user-submitted corrections/modifications to existing serial killers."""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]
    
    killer = models.ForeignKey(
        SerialKiller, 
        on_delete=models.CASCADE, 
        related_name='modifications',
        db_column='killer_id',
        help_text="Serial killer this modification is about"
    )
    suggestion_text = models.TextField(help_text="Correction or modification details")
    submission_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = 'Modifications'
        managed = True
        ordering = ['-created_at']
        verbose_name = 'Modification'
        verbose_name_plural = 'Modifications'
    
    def __str__(self):
        return f"Correction for {self.killer.common_name} - {self.get_submission_status_display()}"
