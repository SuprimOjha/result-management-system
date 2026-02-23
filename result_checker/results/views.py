from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import ExcelUploadForm, ResultSearchForm
from .models import SchoolSettings, StudentResult, ExcelUpload, TeamMember
from .utils import process_excel_file
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
import os

def home(request):
    form = ResultSearchForm()
    return render(request, 'results/home.html', {'form': form})

def search_result(request):
    if request.method == 'POST':
        form = ResultSearchForm(request.POST)
        if form.is_valid():
            symbol_number = form.cleaned_data['symbol_number'].strip()
            
            try:
                result = StudentResult.objects.get(symbol_number=symbol_number)

                context = {
                    'result': result,
                    'symbol_number': symbol_number,
                    'found': True,
                    'school_settings': SchoolSettings.objects.first()
                }

                subjects = []
                for i in range(1, 6):
                    subject_name = getattr(result, f'subject_{i}', '')
                    marks = getattr(result, f'marks_{i}', 0)
                    grade = getattr(result, f'grade_{i}', '')

                    if subject_name:
                        subjects.append({
                            'name': subject_name,
                            'marks': marks,
                            'grade': grade
                        })

                context['subjects'] = subjects

            except StudentResult.DoesNotExist:
                context = {
                    'found': False,
                    'symbol_number': symbol_number,
                    'message': 'No result found for this symbol number.',
                    'school_settings': SchoolSettings.objects.first()
                }

            return render(request, 'results/result_display.html', context)

    return redirect('home')



@login_required
def upload_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        semester = request.POST.get('semester', '')
        program = request.POST.get('program', '')
        
        try:
            # Save the uploaded file
            upload = ExcelUpload.objects.create(
                excel_file=excel_file,
                semester=semester,
                program=program
            )
            
            print(f"\n{'='*60}")
            print(f"UPLOAD DEBUG: Starting file processing")
            print(f"File: {excel_file.name}")
            print(f"Semester: {semester}")
            print(f"Program: {program}")
            print(f"File saved at: {upload.excel_file.path}")
            print(f"{'='*60}\n")
            
            # Process the Excel file
            records_processed = process_excel_file(
                upload.excel_file.path,
                semester,
                program
            )
            
            messages.success(request, f'Successfully processed {records_processed} records!')
            
            # Show summary in console
            print(f"\n{'='*60}")
            print(f"UPLOAD SUMMARY")
            print(f"Records processed: {records_processed}")
            print(f"{'='*60}")
            
            return redirect('upload_excel')
            
        except Exception as e:
            error_msg = f'Error: {str(e)}'
            print(f"\n❌ UPLOAD ERROR: {error_msg}")
            messages.error(request, error_msg)
    
    uploads = ExcelUpload.objects.all().order_by('-uploaded_at')[:10]
    return render(request, 'results/upload_excel.html', {'uploads': uploads})


@login_required
def result_list(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        results = StudentResult.objects.filter(
            Q(symbol_number__icontains=search_query) |
            Q(full_name__icontains=search_query) |
            Q(program__icontains=search_query)
        )
    else:
        results = StudentResult.objects.all()
    
    return render(request, 'results/result_list.html', {
        'results': results,
        'search_query': search_query
    })


@login_required
def result_detail(request, symbol_number):
    result = get_object_or_404(StudentResult, symbol_number=symbol_number)
    
    # Get all subjects
    subjects = []
    for i in range(1, 6):
        subject_name = getattr(result, f'subject_{i}', '')
        if subject_name:
            subjects.append({
                'name': subject_name,
                'marks': getattr(result, f'marks_{i}', 0),
                'grade': getattr(result, f'grade_{i}', '')
            })
    
    return render(request, 'results/result_detail.html', {
        'result': result,
        'subjects': subjects,
        'school_settings': SchoolSettings.objects.first()
    })

def ui(request):
    team_members = TeamMember.objects.all()
    
    # Get school settings (assuming you have only one)
    school_settings = SchoolSettings.objects.first()  # returns None if not set

    context = {
        'team_members': team_members,
        'school_settings': school_settings,  # pass to template
    }
    return render(request, 'results/index.html', context)

def custom_404(request, exception):
    return render(request, "results/404.html", status=404)

@login_required
def admin_dashboard(request):
    return render(request, "results/admin_dashboard.html")

def signup(request):
    if request.method == "POST":
        school_name = request.POST.get("school_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect("signup")

        # Create user
        user = User.objects.create(
            username=email,
            email=email,
            password=make_password(password)
        )

        # Optional: store school_name in profile later
        login(request, user)

        return redirect("admin_panel")

    return render(request, "results/signup.html")

from django.contrib.auth import authenticate, login

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("admin_panel")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")

    return render(request, "results/login.html")