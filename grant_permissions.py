import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from killers.models import Suggestion, Modification, SerialKiller

if len(sys.argv) < 2:
    print("Usage: python grant_permissions.py <username>")
    exit()

staff_username = sys.argv[1]

try:
    staff_user = User.objects.get(username=staff_username)
except User.DoesNotExist:
    print(f"User '{staff_username}' not found!")
    exit()

print(f"Granting permissions to {staff_username}...\n")

# Get content types
suggestion_ct = ContentType.objects.get_for_model(Suggestion)
modification_ct = ContentType.objects.get_for_model(Modification)
serialkiller_ct = ContentType.objects.get_for_model(SerialKiller)

# Define permissions to grant
permissions_to_grant = [
    # Suggestion permissions
    Permission.objects.get(content_type=suggestion_ct, codename='view_suggestion'),
    Permission.objects.get(content_type=suggestion_ct, codename='add_suggestion'),
    Permission.objects.get(content_type=suggestion_ct, codename='change_suggestion'),
    # Modification permissions
    Permission.objects.get(content_type=modification_ct, codename='view_modification'),
    Permission.objects.get(content_type=modification_ct, codename='add_modification'),
    Permission.objects.get(content_type=modification_ct, codename='change_modification'),
    # SerialKiller permissions
    Permission.objects.get(content_type=serialkiller_ct, codename='view_serialkiller'),
    Permission.objects.get(content_type=serialkiller_ct, codename='add_serialkiller'),
    Permission.objects.get(content_type=serialkiller_ct, codename='change_serialkiller'),
]

# Grant permissions
for perm in permissions_to_grant:
    staff_user.user_permissions.add(perm)
    print(f"[OK] Granted: {perm.name}")

print(f"\n[OK] All permissions granted to {staff_username}!")
print(f"\nThe user should now be able to see and edit assigned records in the admin panel.")
