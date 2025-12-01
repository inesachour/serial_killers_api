import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

print("Testing signal for new user...\n")

# Create a test user
test_username = "test_signal_user"

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
print(f"is_superuser: {user.is_superuser}")

# Check permissions
perms = user.user_permissions.all()
print(f"\nPermissions count: {perms.count()}")

if perms.count() > 0:
    print("\nPermissions granted:")
    for perm in perms:
        print(f"  - {perm.name}")
else:
    print("\n[ERROR] No permissions were granted automatically!")
    print("The signal might not be working.")

# Clean up
user.delete()
print(f"\nTest user deleted.")
