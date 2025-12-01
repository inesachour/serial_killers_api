from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Suggestion, Modification, SerialKiller


@receiver(post_save, sender=User)
def grant_staff_permissions(sender, instance, created, **kwargs):
    """
    Automatically assign staff users to the 'Staff' group.
    This runs whenever a User is created or updated.
    """
    # Only for staff users (non-superusers)
    if instance.is_staff and not instance.is_superuser:
        from django.contrib.auth.models import Group
        
        try:
            staff_group = Group.objects.get(name='Staff')
            
            # Add user to group if not already in it
            if not instance.groups.filter(name='Staff').exists():
                instance.groups.add(staff_group)
                print(f"[OK] Added staff user to 'Staff' group: {instance.username}")
                
        except Group.DoesNotExist:
            print("[ERROR] 'Staff' group does not exist! Please run migrations.")
