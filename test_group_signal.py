import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group

print("Testing Group-based signal...\n")

# Create a test user
test_username = "test_group_user"

# Delete if exists
User.objects.filter(username=test_username).delete()

# Create new staff user
print(f"Creating staff user: {test_username}")
user = User.objects.create_user(
    username=test_username,
    password='testpass123',
    is_staff=True
)

print(f"User created: {user.username}")
print(f"is_staff: {user.is_staff}")

# Check groups
groups = user.groups.all()
print(f"\nGroups count: {groups.count()}")

if groups.filter(name='Staff').exists():
    print("[OK] User was automatically added to 'Staff' group!")
    
    # Check permissions inherited from group
    staff_group = groups.get(name='Staff')
    perms = staff_group.permissions.all()
    print(f"\nPermissions inherited from 'Staff' group ({perms.count()}):")
    for perm in perms:
        print(f"  - {perm.name}")
else:
    print("\n[ERROR] User was NOT added to 'Staff' group!")

# Clean up
user.delete()
print(f"\nTest user deleted.")
