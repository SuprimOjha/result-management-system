from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.hashers import make_password

from .forms import ResultSearchForm
from .models import SchoolSettings, StudentResult, ExcelUpload, TeamMember
from .utils import process_excel_file


def home(request):
    form = ResultSearchForm()
    return render(request, 'results/home.html', {'form': form})


def search_result(request):
    if request.method == 'POST':
        form = ResultSearchForm(request.POST)
        if form.is_valid():
            symbol_number = form.cleaned_data['symbol_number'].strip()

            try:
                result = StudentResult.objects.select_related('school').get(symbol_number=symbol_number)
                school_info = result.school or SchoolSettings.objects.first()
                context = {
                    'result': result,
                    'symbol_number': symbol_number,
                    'found': True,
                    'school_settings': school_info,
                }

                subjects = []
                for i in range(1, 6):
                    subject_name = getattr(result, f'subject_{i}', '')
                    marks = getattr(result, f'marks_{i}', 0)
                    grade = getattr(result, f'grade_{i}', '')

                    if subject_name:
                        subjects.append({'name': subject_name, 'marks': marks, 'grade': grade})

                context['subjects'] = subjects

            except StudentResult.DoesNotExist:
                context = {
                    'found': False,
                    'symbol_number': symbol_number,
                    'message': 'No result found for this symbol number.',
                    'school_settings': SchoolSettings.objects.first(),
                }

            return render(request, 'results/result_display.html', context)

    return redirect('home')


@login_required
def upload_excel(request):
    school_settings = SchoolSettings.objects.filter(owner=request.user).first()
    if not school_settings:
        messages.error(request, 'Please complete school signup before uploading results.')
        return redirect('admin_dashboard')

    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        semester = request.POST.get('semester', '')
        program = request.POST.get('program', '')

        try:
            upload = ExcelUpload.objects.create(excel_file=excel_file, semester=semester, program=program)
            records_processed = process_excel_file(upload.excel_file.path, semester, program, school=school_settings)
            messages.success(request, f'Successfully processed {records_processed} records!')
            return redirect('admin_dashboard')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    uploads = ExcelUpload.objects.all().order_by('-uploaded_at')[:10]
    return render(request, 'results/upload_excel.html', {'uploads': uploads})


@login_required
def result_list(request):
    search_query = request.GET.get('search', '')

    results = StudentResult.objects.filter(school__owner=request.user)
    if search_query:
        results = results.filter(
            Q(symbol_number__icontains=search_query)
            | Q(full_name__icontains=search_query)
            | Q(program__icontains=search_query)
        )

    return render(request, 'results/result_list.html', {'results': results, 'search_query': search_query})


@login_required
def result_detail(request, symbol_number):
    result = get_object_or_404(StudentResult, symbol_number=symbol_number, school__owner=request.user)

    subjects = []
    for i in range(1, 6):
        subject_name = getattr(result, f'subject_{i}', '')
        if subject_name:
            subjects.append({'name': subject_name, 'marks': getattr(result, f'marks_{i}', 0), 'grade': getattr(result, f'grade_{i}', '')})

    return render(
        request,
        'results/result_detail.html',
        {'result': result, 'subjects': subjects, 'school_settings': result.school},
    )


def ui(request):
    team_members = TeamMember.objects.all()
    school_settings = SchoolSettings.objects.first()
    published_schools = SchoolSettings.objects.filter(studentresult__isnull=False).distinct().order_by('school_name')

    context = {
        'team_members': team_members,
        'school_settings': school_settings,
        'published_schools': published_schools,
    }
    return render(request, 'results/index.html', context)


def custom_404(request, exception):
    return render(request, 'results/404.html', status=404)


@login_required
def admin_dashboard(request):
    school_settings = SchoolSettings.objects.filter(owner=request.user).first()
    recent_results = StudentResult.objects.filter(school=school_settings).order_by('-updated_at')[:10] if school_settings else []

    if request.method == 'POST' and school_settings:
        school_settings.school_name = request.POST.get('school_name', school_settings.school_name)
        school_settings.address = request.POST.get('address', school_settings.address)
        school_settings.phone = request.POST.get('phone', school_settings.phone)
        school_settings.email = request.POST.get('email', school_settings.email)
        if request.FILES.get('logo'):
            school_settings.logo = request.FILES['logo']
        school_settings.save()
        messages.success(request, 'School profile updated successfully.')
        return redirect('admin_dashboard')

    return render(
        request,
        'results/admin_dashboard.html',
        {
            'school_settings': school_settings,
            'result_count': StudentResult.objects.filter(school=school_settings).count() if school_settings else 0,
            'recent_results': recent_results,
        },
    )


def signup(request):
    if request.method == 'POST':
        school_name = request.POST.get('school_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('signup')

        user = User.objects.create(username=email, email=email, password=make_password(password))
        SchoolSettings.objects.create(owner=user, school_name=school_name, email=email)
        auth_login(request, user)
        return redirect('admin_dashboard')

    return render(request, 'results/signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('admin_dashboard')

        messages.error(request, 'Invalid email or password')
        return redirect('login')

    return render(request, 'results/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')
