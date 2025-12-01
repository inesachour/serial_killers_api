from django.db import connection

def check_columns():
    with connection.cursor() as cursor:
        # Check Suggestions table
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'Suggestions'
            AND column_name LIKE '%assigned%'
        """)
        print("Suggestions table - assigned columns:")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]}")
        
        # Check Modifications table
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'Modifications'
            AND column_name LIKE '%assigned%'
        """)
        print("\nModifications table - assigned columns:")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]}")
        
        # Check Serial Killers table
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'Serial Killers'
            AND column_name LIKE '%assigned%'
        """)
        print("\nSerial Killers table - assigned columns:")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]}")

if __name__ == '__main__':
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    check_columns()
