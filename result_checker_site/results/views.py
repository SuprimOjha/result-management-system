import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from .models import Result, School

# ------------------ MAIN PAGE ------------------




# ------------------ SIGNUP ------------------

def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect("signup")

        otp = random.randint(100000, 999999)

        request.session["signup_email"] = email
        request.session["signup_password"] = password
        request.session["signup_otp"] = otp

        send_mail(
            "Your OTP Code",
            f"Your OTP for account verification is: {otp}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return redirect("verify_otp")

    return render(request, "results/signup.html")


# ------------------ VERIFY OTP ------------------

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        saved_otp = request.session.get("signup_otp")

        if str(entered_otp) == str(saved_otp):
            email = request.session.get("signup_email")
            password = request.session.get("signup_password")

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )

            login(request, user)

            # Clear session
            request.session.flush()

            return redirect("admin_dashboard")

        else:
            messages.error(request, "Invalid OTP")

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
    return render(request, "results/admin_dashboard.html")


def home(request):
    # send schools to populate the dropdown
    schools = School.objects.all()
    return render(request, 'results/index.html', {'schools': schools})

def get_schools(request):
    schools = list(School.objects.values('code', 'name'))
    return JsonResponse({'schools': schools})

def check_result(request):
    symbol = request.GET.get('symbol')
    school_code = request.GET.get('school')
    exam_type = request.GET.get('exam')

    try:
        school = School.objects.get(code=school_code)
        # get the result entered by admin
        result = Result.objects.get(symbol_number=symbol, school=school, exam_type=exam_type)
        data = {
            "name": result.student_name,
            "roll": result.roll_number,
            "symbol": result.symbol_number,
            "department": result.department,
            "semester": result.semester,
            "total": result.total_marks,
            "obtained": result.obtained_marks,
            "grade": result.grade,
            "status": result.status
        }
        return JsonResponse({"success": True, "result": data})
    except (School.DoesNotExist, Result.DoesNotExist):
        return JsonResponse({"success": False})