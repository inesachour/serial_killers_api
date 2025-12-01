import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from killers.models import Suggestion, Modification, SerialKiller

staff_username = input("Enter the staff username: ")

try:
    staff_user = User.objects.get(username=staff_username)
except User.DoesNotExist:
    print(f"User '{staff_username}' not found!")
    exit()

print(f"\n=== Permissions Check for {staff_username} ===\n")

# Check model permissions
permissions_needed = [
    ('killers', 'view_suggestion', 'View Suggestion'),
    ('killers', 'add_suggestion', 'Add Suggestion'),  
    ('killers', 'change_suggestion', 'Change Suggestion'),
    ('killers', 'view_modification', 'View Modification'),
    ('killers', 'add_modification', 'Add Modification'),
    ('killers', 'change_modification', 'Change Modification'),
    ('killers', 'view_serialkiller', 'View Serial Killer'),
    ('killers', 'add_serialkiller', 'Add Serial Killer'),
    ('killers', 'change_serialkiller', 'Change Serial Killer'),
]

has_all_permissions = True
for app, perm_codename, perm_name in permissions_needed:
    has_perm = staff_user.has_perm(f'{app}.{perm_codename}')
    status = "✓" if has_perm else "✗ MISSING"
    if not has_perm:
        has_all_permissions = False
    print(f"{status} {perm_name} ({app}.{perm_codename})")

if not has_all_permissions:
    print("\n⚠️  USER IS MISSING PERMISSIONS!")
    print("\nTo fix this, run the following commands as a superuser in Django admin:")
    print("1. Go to Authentication and Authorization > Users")
    print(f"2. Edit user '{staff_username}'")
    print("3. Scroll to 'User permissions' and add:")
    print("   - killers | suggestion | Can view suggestion")
    print("   - killers | suggestion | Can add suggestion")
    print("   - killers | suggestion | Can change suggestion")
    print("   - killers | modification | Can view modification")
    print("   - killers | modification | Can add modification")
    print("   - killers | modification | Can change modification")
    print("   - killers | serial killer | Can view serial killer")
    print("   - killers | serial killer | Can add serial killer")
    print("   - killers | serial killer | Can change serial killer")
    print("\nOr run this script to grant all permissions automatically:")
    print(f"\npython grant_permissions.py {staff_username}")
else:
    print("\n✓ User has all necessary permissions!")
