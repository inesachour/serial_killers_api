from django.db import migrations

def create_staff_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    
    # Create or get the group
    staff_group, created = Group.objects.get_or_create(name='Staff')
    
    # Get content types
    Suggestion = apps.get_model('killers', 'Suggestion')
    Modification = apps.get_model('killers', 'Modification')
    SerialKiller = apps.get_model('killers', 'SerialKiller')
    
    suggestion_ct = ContentType.objects.get_for_model(Suggestion)
    modification_ct = ContentType.objects.get_for_model(Modification)
    serialkiller_ct = ContentType.objects.get_for_model(SerialKiller)
    
    # Get permissions
    permissions = []
    for ct in [suggestion_ct, modification_ct, serialkiller_ct]:
        permissions.extend(Permission.objects.filter(content_type=ct))
        
    # Assign permissions to group
    staff_group.permissions.set(permissions)
    print(f"Updated 'Staff' group with {len(permissions)} permissions")

def remove_staff_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name='Staff').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('killers', '0006_remove_duplicate_assigned_to_columns'),
    ]

    operations = [
        migrations.RunPython(create_staff_group, remove_staff_group),
    ]
