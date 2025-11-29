from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from .services import get_supabase_client

def docs_view(request):
    return render(request, 'documentation.html')

def home_view(request):
    return render(request, 'home.html')

def suggestion_view(request):
    if request.method == 'POST':
        try:
            supabase = get_supabase_client()
            form_type = request.POST.get('form_type')

            if form_type == 'new_killer':
                data = {
                    'common_name': request.POST.get('common_name'),
                    'full_name': request.POST.get('full_name'),
                    'aliases': request.POST.get('aliases'),
                    'date_of_birth': request.POST.get('date_of_birth'),
                    'birth_country': request.POST.get('birth_country'),
                    'gender': request.POST.get('gender'),
                    'proven_victims': request.POST.get('proven_victims'),
                    'possible_victims': request.POST.get('possible_victims'),
                    'years_active': request.POST.get('years_active'),
                    'active_countries': request.POST.get('active_countries'),
                    'modus_operandi': request.POST.get('modus_operandi'),
                    'capture_date': request.POST.get('capture_date'),
                    'sentence': request.POST.get('sentence'),
                    'death_date': request.POST.get('death_date'),
                    'manner_of_death': request.POST.get('manner_of_death'),
                    'status': request.POST.get('status'),
                    'notes': request.POST.get('notes'),
                    'submission_status': 'new'
                }
                # Remove empty fields
                data = {k: v for k, v in data.items() if v}
                supabase.table('Suggestions').insert(data).execute()
                return render(request, 'suggestion.html', {'message': 'Suggestion submitted successfully!'})

            elif form_type == 'correction':
                data = {
                    'killer_id': request.POST.get('killer_id'),
                    'suggestion_text': request.POST.get('suggestion_text'),
                    'submission_status': 'new'
                }
                supabase.table('Modifications').insert(data).execute()
                # Re-fetch killers for the dropdown
                response = supabase.table('Serial Killers').select("id, common_name").order('common_name').execute()
                killers = response.data
                return render(request, 'suggestion.html', {'message': 'Correction submitted successfully!', 'killers': killers, 'is_correction': True})

        except Exception as e:
            context = {'error': str(e)}
            if request.POST.get('form_type') == 'correction':
                context['is_correction'] = True
                try:
                    # Re-fetch killers so the dropdown doesn't disappear
                    response = supabase.table('Serial Killers').select("id, common_name").order('common_name').execute()
                    context['killers'] = response.data
                except:
                    pass
            return render(request, 'suggestion.html', context)

    # GET request
    is_correction = request.GET.get('type') == 'correction'
    killers = []
    if is_correction:
        try:
            supabase = get_supabase_client()
            response = supabase.table('Serial Killers').select("id, common_name").order('common_name').execute()
            killers = response.data
        except Exception as e:
            print(f"Error fetching killers: {e}")

    return render(request, 'suggestion.html', {'is_correction': is_correction, 'killers': killers})

@api_view(['GET'])
def get_all_killers(request):
    """
    Fetch all serial killers from Supabase.
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table('Serial Killers').select("*").execute()
        return Response(response.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_killer_by_name(request, common_name):
    """
    Fetch a specific serial killer by name (ilike search).
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table('Serial Killers').select("*").ilike('common_name', f"%{common_name}%").execute()
        return Response(response.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def dashboard_view(request):
    try:
        supabase = get_supabase_client()
        
        # Fetch suggestions
        suggestions_response = supabase.table('Suggestions').select("*").execute()
        suggestions = suggestions_response.data
        
        # Fetch modifications
        modifications_response = supabase.table('Modifications').select("*").execute()
        modifications = modifications_response.data
        
        # Fetch all killers with all fields for statistics
        killers_response = supabase.table('Serial Killers').select("*").execute()
        killers = killers_response.data
        killers_map = {k['id']: k['common_name'] for k in killers}
        
        for mod in modifications:
            mod['killer_name'] = killers_map.get(mod['killer_id'], 'Unknown ID')

        # Calculate Serial Killers Statistics
        total_killers = len(killers)
        
        # Country distribution
        country_counts = {}
        for killer in killers:
            country = killer.get('country', 'Unknown')
            if country:
                country_counts[country] = country_counts.get(country, 0) + 1
        
        # Sort countries by count and get top 5
        top_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Gender distribution
        gender_counts = {}
        for killer in killers:
            gender = killer.get('gender', 'Unknown')
            if gender:
                gender_counts[gender] = gender_counts.get(gender, 0) + 1
        
        # Modus Operandi categories (top 5)
        mo_counts = {}
        for killer in killers:
            mo = killer.get('modus_operandi', '')
            if mo:
                mo_counts[mo] = mo_counts.get(mo, 0) + 1
        top_mo = sorted(mo_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Parse years_active to find most active decade
        decades_count = {}
        for killer in killers:
            years_active = killer.get('years_active', '')
            if years_active and '-' in years_active:
                try:
                    # Parse format like "1974-1978"
                    parts = years_active.split('-')
                    start_year = int(parts[0].strip())
                    # Determine decade (e.g., 1970s)
                    decade = (start_year // 10) * 10
                    decades_count[decade] = decades_count.get(decade, 0) + 1
                except:
                    pass
        
        # Get most active decade
        most_active_decade = None
        if decades_count:
            most_active_decade = max(decades_count.items(), key=lambda x: x[1])
        
        
        # Helper function to parse victim counts (handles "100+", "17", etc.)
        def parse_victim_count(value):
            if not value:
                return 0
            # Convert to string and remove whitespace
            value_str = str(value).strip()
            # Extract numeric part (handles "100+", "50-60", etc.)
            import re
            match = re.search(r'(\d+)', value_str)
            if match:
                return int(match.group(1))
            return 0
        
        # Victim statistics
        total_proven_victims = 0
        total_possible_victims = 0
        for killer in killers:
            proven = killer.get('proven_victims')
            possible = killer.get('possible_victims')
            
            total_proven_victims += parse_victim_count(proven)
            total_possible_victims += parse_victim_count(possible)


        # Group submissions by status
        dashboard_data = {
            'new': [],
            'in_progress': [],
            'finished': []
        }
        
        def add_to_dashboard(item, type_label):
            item['type'] = type_label
            item_status = item.get('submission_status', 'new')
            if item_status == 'new':
                dashboard_data['new'].append(item)
            elif item_status == 'in_progress':
                dashboard_data['in_progress'].append(item)
            elif item_status == 'finished':
                dashboard_data['finished'].append(item)
            else:
                # Fallback for unknown statuses
                dashboard_data['new'].append(item)

        for s in suggestions:
            add_to_dashboard(s, 'Suggestion')
            
        for m in modifications:
            add_to_dashboard(m, 'Correction')
        
        # Calculate submission statistics by type
        suggestions_new = sum(1 for item in dashboard_data['new'] if item['type'] == 'Suggestion')
        suggestions_progress = sum(1 for item in dashboard_data['in_progress'] if item['type'] == 'Suggestion')
        suggestions_done = sum(1 for item in dashboard_data['finished'] if item['type'] == 'Suggestion')
        
        corrections_new = sum(1 for item in dashboard_data['new'] if item['type'] == 'Correction')
        corrections_progress = sum(1 for item in dashboard_data['in_progress'] if item['type'] == 'Correction')
        corrections_done = sum(1 for item in dashboard_data['finished'] if item['type'] == 'Correction')
        
        # Prepare context
        context = {
            'dashboard_data': dashboard_data,
            'killer_stats': {
                'total': total_killers,
                'top_countries': top_countries,
                'gender_distribution': gender_counts,
                'top_mo': top_mo,
                'most_active_decade': most_active_decade,
                'total_proven_victims': total_proven_victims,
                'total_possible_victims': total_possible_victims,
            },
            'submission_stats': {
                'suggestions_new': suggestions_new,
                'suggestions_progress': suggestions_progress,
                'suggestions_done': suggestions_done,
                'corrections_new': corrections_new,
                'corrections_progress': corrections_progress,
                'corrections_done': corrections_done,
            }
        }
            
        return render(request, 'dashboard.html', context)

    except Exception as e:
        return render(request, 'dashboard.html', {'error': str(e)})

def update_status_view(request):
    if request.method == 'POST':
        try:
            supabase = get_supabase_client()
            item_id = request.POST.get('id')
            item_type = request.POST.get('type')
            new_status = request.POST.get('status')
            
            table_name = 'Suggestions' if item_type == 'Suggestion' else 'Modifications'
            
            supabase.table(table_name).update({'submission_status': new_status}).eq('id', item_id).execute()
            
        except Exception as e:
            print(f"Error updating status: {e}")
            
    return redirect('dashboard')
