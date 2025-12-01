import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from killers.models import Suggestion, Modification
from django.contrib.auth.models import User

# Get or create a test user
test_user, created = User.objects.get_or_create(
    username='test_staff',
    defaults={'is_staff': True}
)

print(f"Test user: {test_user.username} (ID: {test_user.id})")

# Try to get a suggestion and check its assigned_to
if Suggestion.objects.exists():
    suggestion = Suggestion.objects.first()
    print(f"\nSuggestion: {suggestion.common_name}")
    print(f"  assigned_to field: {suggestion.assigned_to}")
    print(f"  assigned_to_id: {suggestion.assigned_to_id}")
    
    # Try assigning
    suggestion.assigned_to = test_user
    suggestion.save()
    
    # Reload and check
    suggestion.refresh_from_db()
    print(f"\nAfter assignment:")
    print(f"  assigned_to field: {suggestion.assigned_to}")
    print(f"  assigned_to_id: {suggestion.assigned_to_id}")
    
    # Check in database directly
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT assigned_to, assigned_to_id FROM \"Suggestions\" WHERE id = {suggestion.id}")
        row = cursor.fetchone()
        print(f"\n  Database columns:")
        print(f"    assigned_to: {row[0]}")
        print(f"    assigned_to_id: {row[1]}")
else:
    print("No suggestions found in database")
