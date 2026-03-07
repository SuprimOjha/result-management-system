import random
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import Result, School, UserProfile, Blog, BlogCategory, TeamMember
import string
import random

def _generate_school_code(name: str) -> str:
    """Produce a short unique code for a school based on its name."""
    # take alphanumeric characters from name, uppercase, first 4
    base = ''.join(ch for ch in name if ch.isalnum()).upper()[:4]
    if not base:
        base = 'SCH'
    code = base
    # ensure uniqueness by appending digits if needed
    while School.objects.filter(code=code).exists():
        suffix = ''.join(random.choices(string.digits, k=2))
        code = f"{base}{suffix}"
    return code

# ------------------ MAIN PAGE ------------------




# ------------------ SIGNUP ------------------

def signup(request):
    if request.method == "POST":
        try:
            email = request.POST.get("email", "").strip()
            password = request.POST.get("password", "").strip()
            full_name = request.POST.get("full_name", "").strip()
            school_name = request.POST.get("school", "").strip()

            # Validate inputs
            if not email or not password:
                messages.error(request, "Email and password are required")
                return redirect("signup")

            if not school_name:
                messages.error(request, "Please provide a school name")
                return redirect("signup")

            # Check if email already registered
            if User.objects.filter(username=email).exists():
                messages.error(request, "Email already registered")
                return redirect("signup")

            # Generate OTP
            otp = random.randint(100000, 999999)

            # Store data in session
            request.session["signup_email"] = email
            request.session["signup_password"] = password
            request.session["signup_full_name"] = full_name
            request.session["signup_school"] = school_name
            request.session["signup_otp"] = otp
            request.session.set_expiry(600)  # OTP valid for 10 minutes

            # Try to send OTP email
            try:
                send_mail(
                    "Your OTP Code",
                    f"Your OTP for account verification is: {otp}\n\nThis OTP is valid for 10 minutes.",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                return redirect("verify_otp")
            except Exception as email_error:
                # If email fails, still allow OTP verification but show warning
                messages.warning(request, "Could not send OTP via email. Please check admin settings.")
                print(f"Email error: {str(email_error)}")  # Log for debugging
                return redirect("verify_otp")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect("signup")

    return render(request, "results/signup.html")


# ------------------ VERIFY OTP ------------------

def verify_otp(request):
    if request.method == "POST":
        try:
            # Reconstruct OTP from individual digit inputs
            otp_digits = [request.POST.get(f'd{i}', '') for i in range(1, 7)]
            entered_otp = ''.join(otp_digits)
            
            saved_otp = request.session.get("signup_otp")

            if str(entered_otp) == str(saved_otp):
                # Get session data with validation
                email = request.session.get("signup_email")
                password = request.session.get("signup_password")
                full_name = request.session.get("signup_full_name") or ""
                school_name = request.session.get("signup_school")

                # Validate required session data
                if not email or not password:
                    messages.error(request, "Session expired. Please sign up again.")
                    return redirect("signup")

                # Check if user already exists
                if User.objects.filter(username=email).exists():
                    messages.error(request, "This email has already been registered.")
                    return redirect("login")

                try:
                    # Create user
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=password,
                        first_name=full_name,
                    )
                except Exception as e:
                    messages.error(request, f"Failed to create account: {str(e)}")
                    return redirect("signup")

                # Look up or create school
                school = None
                if school_name:
                    try:
                        school, created = School.objects.get_or_create(
                            name=school_name,
                            defaults={'code': _generate_school_code(school_name)}
                        )
                        # If school existed but has no code, generate one
                        if not school.code:
                            school.code = _generate_school_code(school_name)
                            school.save()
                    except Exception as e:
                        messages.warning(request, f"Could not link school: {str(e)}")
                        school = None

                # Create UserProfile
                try:
                    UserProfile.objects.create(user=user, school=school)
                except Exception as e:
                    messages.warning(request, f"Profile creation issue: {str(e)}")

                # Login user
                login(request, user)
                
                # Clear session
                request.session.flush()

                messages.success(request, "Account created successfully!")
                return redirect("admin_dashboard")

            else:
                messages.error(request, "Invalid OTP. Please try again.")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, "results/verify_otp.html")


# ------------------ LOGIN ------------------

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "results/login.html")


# ------------------ LOGOUT ------------------

def logout_view(request):
    logout(request)
    return redirect("home")


# ------------------ ADMIN DASHBOARD ------------------

@login_required
def admin_dashboard(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        school = user_profile.school if user_profile else None
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
        school = None

    # only provide list of schools if user has not yet been tied to one
    if school:
        schools = []
    else:
        schools = School.objects.all()

    # Get user's full name (first name and last name)
    user_full_name = request.user.get_full_name() or request.user.first_name or request.user.username
    school_name = school.name if school else "No School Assigned"
    
    context = {
        'school': school,
        'schools': schools,
        'user_full_name': user_full_name,
        'school_name': school_name,
        'initials': ''.join([word[0].upper() for word in user_full_name.split()[:2]])
    }

    return render(request, "results/admin_dashboard.html", context)


@login_required
def upload_excel(request):
    if request.method == 'POST':
        # Handle file upload
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            messages.error(request, 'Please select an Excel file.')
            return redirect('upload_excel')
        
        try:
            import pandas as pd
            df = pd.read_excel(excel_file)
            
            # Process the dataframe similar to the bulk save
            results = []
            for _, row in df.iterrows():
                name = row.get('name', '')
                roll = str(row.get('roll', ''))
                symbol = str(row.get('symbol', ''))
                dept = row.get('department', '')
                sem = row.get('semester', '')
                total = float(row.get('total', 0))
                obtained = float(row.get('obtained', 0))
                pct_val = round(obtained / total * 100) if total > 0 else 0
                grade_val = 'A' if pct_val >= 90 else 'B' if pct_val >= 75 else 'C' if pct_val >= 55 else 'D' if pct_val >= 40 else 'F'
                status_val = 'Pass' if pct_val >= 40 else 'Fail'
                
                results.append({
                    'name': name,
                    'roll': roll,
                    'symbol': symbol,
                    'dept': dept,
                    'sem': sem,
                    'total': total,
                    'obtained': obtained,
                    'pct': pct_val,
                    'grade': grade_val,
                    'status': status_val,
                    'year': '',
                    'examType': 'Final Examination',
                    'subjects': []
                })
            
            # Save using the bulk API
            from django.http import JsonResponse
            result = api_bulk_save_results(request._get_raw_host(), results)  # Need to adjust
            
            # Since it's a view, not API, handle differently
            # For simplicity, use the function directly
            saved_results = []
            for res in results:
                result_obj = Result.objects.create(
                    school=request.user.profile.school,
                    student_name=res['name'],
                    roll_number=res['roll'],
                    symbol_number=res['symbol'],
                    semester=res['sem'],
                    exam_type=res['examType'],
                    total_marks=res['total'],
                    obtained_marks=res['obtained'],
                    department=res['dept'],
                    grade=res['grade'],
                    status=res['status']
                )
                saved_results.append(result_obj)
            
            messages.success(request, f'Successfully uploaded {len(saved_results)} results.')
            return redirect('admin_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')
            return redirect('upload_excel')
    
    return render(request, 'results/upload_excel.html')


def home(request):
    # send schools to populate the dropdown
    schools = School.objects.all()
    team_members = TeamMember.objects.all()
    return render(request, 'results/index.html', {
        'schools': schools,
        'team_members': team_members
    })

def get_schools(request):
    schools = list(School.objects.values('id', 'code', 'name'))
    return JsonResponse({'schools': schools})

def check_result(request):
    symbol = request.GET.get('symbol')
    school_id = request.GET.get('school')

    try:
        school = School.objects.get(id=school_id)
        # Get the first result matching symbol and school (ignoring exam type)
        result = Result.objects.filter(symbol_number=symbol, school=school).first()
        
        if not result:
            return JsonResponse({"success": False, "error": "Result not found"})
        
        # Calculate percentage
        pct = round(result.obtained_marks / result.total_marks * 100) if result.total_marks > 0 else 0
        
        data = {
            "name": result.student_name,
            "roll": result.roll_number,
            "symbol": result.symbol_number,
            "department": result.department,
            "semester": result.semester,
            "total": result.total_marks,
            "obtained": result.obtained_marks,
            "percentage": pct,
            "grade": result.grade,
            "status": result.status
        }
        return JsonResponse({"success": True, "result": data})
    except School.DoesNotExist:
        return JsonResponse({"success": False, "error": "School not found"})


# ───────────────── API ENDPOINTS FOR DASHBOARD ──────────────

@login_required
def api_get_results(request):
    """Get all results for the logged-in user's school"""
    try:
        # Get the admin's school from their profile
        try:
            profile = request.user.profile
            school = profile.school
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
            school = profile.school
        
        if not school:
            return JsonResponse({'success': True, 'results': []})
        
        results = Result.objects.filter(school=school).values(
            'id', 'student_name', 'roll_number', 'symbol_number', 
            'semester', 'exam_type', 'total_marks', 'obtained_marks', 
            'department', 'grade', 'status', 'school__name', 'school__code'
        )
        results_list = list(results)
        
        # Calculate percentage and ensure all fields
        for r in results_list:
            if r['total_marks'] > 0:
                r['pct'] = round(r['obtained_marks'] / r['total_marks'] * 100)
            else:
                r['pct'] = 0
            # Rename fields to match frontend expectations
            r['name'] = r.pop('student_name')
            r['roll'] = r.pop('roll_number')
            r['symbol'] = r.pop('symbol_number')
            r['sem'] = r.pop('semester')
            r['examType'] = r.pop('exam_type')
            r['total'] = r.pop('total_marks')
            r['obtained'] = r.pop('obtained_marks')
            r['dept'] = r.pop('department')
            r['school'] = r.pop('school__name')
            r['schoolCode'] = r.pop('school__code')
        
        return JsonResponse({'success': True, 'results': results_list})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def api_save_result(request):
    """Save a single result to the database"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields - check for existence, not truthiness
        required_fields = ['name', 'roll', 'symbol']
        for field in required_fields:
            if field not in data or data.get(field) is None or str(data.get(field)).strip() == '':
                return JsonResponse({'success': False, 'error': f'{field} is required'}, status=400)
        
        # Validate numeric fields
        try:
            total = int(data.get('total', 0))
            obtained = int(data.get('obtained', 0))
            if total <= 0:
                return JsonResponse({'success': False, 'error': 'Total marks must be greater than 0'}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'Total and obtained marks must be valid numbers'}, status=400)
        
        # Get the admin's school from their profile
        try:
            profile = request.user.profile
            school = profile.school
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
            school = profile.school
        
        if not school:
            return JsonResponse({'success': False, 'error': 'Please set your school first'}, status=400)
        
        # Calculate grade and status
        pct = round(obtained / total * 100) if total > 0 else 0
        grade = 'A' if pct >= 90 else 'B' if pct >= 75 else 'C' if pct >= 55 else 'D' if pct >= 40 else 'F'
        status = 'Pass' if pct >= 40 else 'Fail'
        
        # Check if result already exists
        existing = Result.objects.filter(
            symbol_number=str(data.get('symbol')).strip(),
            school=school,
            exam_type=data.get('examType', 'Final Examination')
        ).first()
        
        if existing:
            # Update existing
            existing.student_name = str(data.get('name')).strip()
            existing.roll_number = str(data.get('roll')).strip()
            existing.semester = data.get('sem', '')
            existing.total_marks = total
            existing.obtained_marks = obtained
            existing.department = data.get('dept', '')
            existing.grade = grade
            existing.status = status
            existing.save()
        else:
            # Create new
            result = Result(
                school=school,
                student_name=str(data.get('name')).strip(),
                roll_number=str(data.get('roll')).strip(),
                symbol_number=str(data.get('symbol')).strip(),
                semester=data.get('sem', ''),
                exam_type=data.get('examType', 'Final Examination'),
                total_marks=total,
                obtained_marks=obtained,
                department=data.get('dept', ''),
                grade=grade,
                status=status
            )
            result.save()
        
        return JsonResponse({'success': True, 'message': 'Result saved successfully'})
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'}, status=400)


@login_required
@require_http_methods(["POST"])
def api_bulk_save_results(request):
    """Save multiple results from Excel upload"""
    try:
        data = json.loads(request.body)
        results_data = data.get('results', [])
        
        if not results_data:
            return JsonResponse({'success': False, 'error': 'No results provided'}, status=400)
        
        # Get the admin's school from their profile
        try:
            profile = request.user.profile
            school = profile.school
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
            school = profile.school
        
        if not school:
            return JsonResponse({'success': False, 'error': 'Please set your school first'}, status=400)
        
        created_count = 0
        updated_count = 0
        errors = []
        
        for idx, row_data in enumerate(results_data):
            try:
                # Validate required fields
                if not row_data.get('name') or not row_data.get('symbol'):
                    errors.append(f'Row {idx + 1}: Name and Symbol are required')
                    continue
                
                total = int(row_data.get('total', 0))
                obtained = int(row_data.get('obtained', 0))
                
                # Calculate grade and status
                pct = round(obtained / total * 100) if total > 0 else 0
                grade = 'A' if pct >= 90 else 'B' if pct >= 75 else 'C' if pct >= 55 else 'D' if pct >= 40 else 'F'
                status = 'Pass' if pct >= 40 else 'Fail'
                
                # Check if result exists
                existing = Result.objects.filter(
                    symbol_number=row_data.get('symbol'),
                    school=school,
                    exam_type=row_data.get('examType', 'Regular')
                ).first()
                
                if existing:
                    # Update
                    existing.student_name = row_data.get('name')
                    existing.roll_number = row_data.get('roll', '')
                    existing.semester = row_data.get('sem', '')
                    existing.total_marks = total
                    existing.obtained_marks = obtained
                    existing.department = row_data.get('dept', '')
                    existing.grade = grade
                    existing.status = status
                    existing.save()
                    updated_count += 1
                else:
                    # Create new
                    result = Result(
                        school=school,
                        student_name=row_data.get('name'),
                        roll_number=row_data.get('roll', ''),
                        symbol_number=row_data.get('symbol'),
                        semester=row_data.get('sem', ''),
                        exam_type=row_data.get('examType', 'Regular'),
                        total_marks=total,
                        obtained_marks=obtained,
                        department=row_data.get('dept', ''),
                        grade=grade,
                        status=status
                    )
                    result.save()
                    created_count += 1
            
            except Exception as e:
                errors.append(f'Row {idx + 1}: {str(e)}')
        
        return JsonResponse({
            'success': True,
            'message': f'Imported {created_count} new results, updated {updated_count}',
            'created': created_count,
            'updated': updated_count,
            'errors': errors
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_http_methods(["DELETE", "POST"])
def api_delete_result(request, result_id):
    """Delete a result"""
    try:
        result = Result.objects.get(id=result_id)
        result.delete()
        return JsonResponse({'success': True, 'message': 'Result deleted successfully'})
    except Result.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Result not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
@require_http_methods(["POST"])
def api_add_school(request):
    """Add a new school"""
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        
        if not name:
            return JsonResponse({'success': False, 'error': 'School name required'}, status=400)
        
        # Check if school already exists (case insensitive)
        if School.objects.filter(name__iexact=name).exists():
            return JsonResponse({'success': False, 'error': 'School already exists'}, status=400)
        
        code = _generate_school_code(name)
        school = School.objects.create(name=name, code=code)
        return JsonResponse({'success': True, 'message': 'School added successfully', 'school': {'id': school.id, 'name': school.name, 'code': school.code}})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
@require_http_methods(["POST"])
def api_set_school(request):
    """Set the user's school. Once a school is assigned it cannot be changed by the admin."""
    try:
        data = json.loads(request.body)
        school_id = data.get('school_id')
        
        if not school_id:
            return JsonResponse({'success': False, 'error': 'School ID required'}, status=400)
        
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        if user_profile.school:
            return JsonResponse({'success': False, 'error': 'School already assigned'}, status=403)

        school = School.objects.get(id=school_id)
        user_profile.school = school
        user_profile.save()
        
        return JsonResponse({'success': True, 'message': 'School set successfully'})
    except School.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'School not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def blog_list(request):
    """Display all published blog posts"""
    page_num = request.GET.get('page', 1)
    category_slug = request.GET.get('category')
    
    # Get all published blogs
    blogs = Blog.objects.filter(is_published=True).order_by('-created_at')
    
    # Filter by category if provided
    current_category = None
    if category_slug:
        current_category = get_object_or_404(BlogCategory, slug=category_slug)
        blogs = blogs.filter(category=current_category)
    
    # Get featured post
    featured_post = blogs.filter(featured=True).first()
    if featured_post:
        blogs = blogs.exclude(id=featured_post.id)
    
    # Get all categories for filter
    categories = BlogCategory.objects.all()
    
    # Paginate results
    paginator = Paginator(blogs, 6)  # 6 posts per page
    page_obj = paginator.get_page(page_num)
    
    context = {
        'featured_post': featured_post,
        'posts': page_obj,
        'categories': categories,
        'current_category': current_category,
    }
    
    return render(request, 'results/blogs.html', context)


def blog_list_by_category(request, slug):
    """Display blogs filtered by category"""
    category = get_object_or_404(BlogCategory, slug=slug)
    page_num = request.GET.get('page', 1)
    
    # Get blogs for this category
    blogs = Blog.objects.filter(category=category, is_published=True).order_by('-created_at')
    
    # Get featured post for this category
    featured_post = blogs.filter(featured=True).first()
    if featured_post:
        blogs = blogs.exclude(id=featured_post.id)
    
    # Get all categories
    categories = BlogCategory.objects.all()
    
    # Paginate
    paginator = Paginator(blogs, 6)
    page_obj = paginator.get_page(page_num)
    
    context = {
        'featured_post': featured_post,
        'posts': page_obj,
        'categories': categories,
        'current_category': category,
    }
    
    return render(request, 'results/blogs.html', context)


def blog_detail(request, slug):
    """Display detailed blog post view"""
    post = get_object_or_404(Blog, slug=slug, is_published=True)
    
    # Increment view count
    post.views += 1
    post.save(update_fields=['views'])
    
    # Get related posts from same category
    related_posts = Blog.objects.filter(
        category=post.category,
        is_published=True
    ).exclude(id=post.id).order_by('-created_at')[:3]
    
    # Get latest posts for sidebar
    latest_posts = Blog.objects.filter(is_published=True).order_by('-created_at')[:5]
    
    # Get all categories for sidebar
    categories = BlogCategory.objects.all()
    
    # Process tags from meta_keywords
    tags = [tag.strip() for tag in post.meta_keywords.split(',') if tag.strip()] if post.meta_keywords else []
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'latest_posts': latest_posts,
        'all_categories': categories,
        'tags': tags,
    }
    
    return render(request, 'results/blogs_detail.html', context)