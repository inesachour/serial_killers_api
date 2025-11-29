# Django Admin Setup Guide

## Step 1: Add Supabase Database Credentials to .env

Add the following lines to your `.env` file with your actual Supabase pooler connection details:

```env
# Supabase PostgreSQL Pooler Connection (Transaction Mode)
SUPABASE_DB_HOST=your-pooler-host.pooler.supabase.com
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres.your-project-ref
SUPABASE_DB_PASSWORD=your-database-password
SUPABASE_DB_PORT=6543
```

### Where to find these values:

1. Go to your Supabase project dashboard
2. Navigate to **Settings** → **Database**
3. Scroll to **Connection Pooling** section
4. Select **Transaction** mode
5. Copy the connection string - it will look like:
   ```
   postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-0-us-xxxx.pooler.supabase.com:6543/postgres
   ```
6. Extract the values:
   - **Host**: everything between `@` and `:6543` (e.g., `aws-0-us-xxxx.pooler.supabase.com`)
   - **User**: everything between `postgresql://` and `:[YOUR-PASSWORD]` (e.g., `postgres.xxxxx`)
   - **Password**: your database password
   - **Port**: `6543` (pooler transaction mode port)
   - **Name**: `postgres`

## Step 2: Install Dependencies

```bash
pip install psycopg2-binary
```

## Step 3: Create Migrations (DO NOT APPLY)

Since your tables already exist in Supabase, we'll create migrations but mark them as "fake" so Django knows about the tables without trying to create them:

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations as "fake" (tells Django tables exist without creating them)
python manage.py migrate --fake-initial
```

⚠️ **IMPORTANT**: The `--fake-initial` flag tells Django the tables already exist. This prevents Django from trying to create tables in Supabase.

## Step 4: Create Admin Superuser

Create an admin account to access Django Admin:

```bash
python manage.py createsuperuser
```

You'll be prompted to enter:
- Username
- Email (optional)
- Password

## Step 5: Run the Development Server

```bash
python manage.py runserver
```

## Step 6: Access Django Admin

1. Open your browser and go to: `http://localhost:8000/admin/`
2. Login with the superuser credentials you created
3. You should see three sections:
   - **Serial Killers** - View and edit all serial killers
   - **Suggestions** - Manage user-submitted suggestions
   - **Modifications** - Manage user-submitted corrections

## Features Available in Django Admin

### Serial Killers
- Search by name or aliases
- Filter by gender, status, country
- Organized form with fieldsets (Personal Info, Crime Details, Legal Status)
- View all details in one place

### Suggestions
- Filter by submission status (New, In Progress, Finished)
- Bulk actions to mark multiple suggestions as in progress or finished
- Date hierarchy to browse by submission date
- Search by name

### Modifications
- Filter by submission status
- Bulk actions to change status
- See which serial killer each modification is about
- Preview of suggestion text

## Troubleshooting

### Connection Error
- Double-check your `.env` file has the correct credentials
- Ensure you're using the **pooler connection** (port 6543), not direct connection
- Verify SSL is not blocked by firewall

### Migration Error
- If you get "table already exists" error, you forgot to use `--fake-initial`
- Run: `python manage.py migrate --fake-initial`

### Can't Login
- Make sure you created a superuser: `python manage.py createsuperuser`
- Check username and password are correct
