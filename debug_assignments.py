import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from killers.models import Suggestion, Modification, SerialKiller
from django.contrib.auth.models import User

# Ask for the staff username
staff_username = input("Enter the staff username: ")

try:
    staff_user = User.objects.get(username=staff_username)
except User.DoesNotExist:
    print(f"User '{staff_username}' not found!")
    exit()

print(f"\n=== User Info ===")
print(f"Username: {staff_user.username}")
print(f"ID: {staff_user.id}")
print(f"is_staff: {staff_user.is_staff}")
print(f"is_superuser: {staff_user.is_superuser}")

print(f"\n=== Assigned Records ===")

# Check Suggestions
suggestions = Suggestion.objects.filter(assigned_to=staff_user)
print(f"\nSuggestions assigned to {staff_username}: {suggestions.count()}")
for s in suggestions:
    print(f"  - {s.common_name} (ID: {s.id}, assigned_to_id: {s.assigned_to_id})")

# Check all suggestions to see assignments
print(f"\nAll Suggestions in database:")
for s in Suggestion.objects.all()[:5]:
    print(f"  - {s.common_name}: assigned_to={s.assigned_to}, assigned_to_id={s.assigned_to_id}")

# Check Modifications
modifications = Modification.objects.filter(assigned_to=staff_user)
print(f"\nModifications assigned to {staff_username}: {modifications.count()}")
for m in modifications:
    print(f"  - {m.killer.common_name} (ID: {m.id}, assigned_to_id: {m.assigned_to_id})")

print(f"\nAll Modifications in database:")
for m in Modification.objects.all()[:5]:
    print(f"  - {m.killer.common_name}: assigned_to={m.assigned_to}, assigned_to_id={m.assigned_to_id}")

# Check Serial Killers
from django.db.models import Q
killers = SerialKiller.objects.filter(
    Q(assigned_to=staff_user) | Q(modifications__assigned_to=staff_user)
).distinct()
print(f"\nSerial Killers accessible to {staff_username}: {killers.count()}")
for k in killers:
    print(f"  - {k.common_name} (ID: {k.id}, assigned_to_id: {k.assigned_to_id})")

print(f"\nAll Serial Killers in database:")
for k in SerialKiller.objects.all()[:5]:
    print(f"  - {k.common_name}: assigned_to={k.assigned_to}, assigned_to_id={k.assigned_to_id}")
