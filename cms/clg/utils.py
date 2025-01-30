from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from .models import Re,Student
import random
from datetime import datetime
def check_user_logged_in(request):
    if 'user_id' not in request.session:
        return False

    # Update last activity timestamp
    request.session['last_activity'] = datetime.now().timestamp()
    return True


def send_otp_email(email, otp):
    subject = "Your OTP for Student Registration - Avanthi College"
    body = f"""
        Dear Student,

        Welcome to Avanthi College, Garividi, Vizianagaram!

        Please use the following OTP to complete your registration:

        OTP: {otp}

        This OTP is valid for 5 minutes. Do not share it with anyone.

        Regards,
        Admissions Team
    """

    from django.core.mail import send_mail
    try:
        send_mail(
            subject,
            body,
            'chganapathi4225@gmail.com',  # Replace with your sender email
            [email],
            fail_silently=False,
        )
    except Exception as e:
        raise Exception(f"Failed to send OTP: {e}")


# Helper function to validate OTP
def validate_otp(request):
    user_otp = request.POST.get('otp')
    session_otp = request.session.get('otp')
    otp_timestamp = request.session.get('otp_timestamp')

    # Validate OTP expiration
    if not otp_timestamp or (now().timestamp() - otp_timestamp > 300):  # 5 minutes expiration time
        return False, "OTP expired. Please request a new OTP."

    # Validate OTP correctness
    if user_otp != session_otp:
        return False, "Invalid OTP. Please check and try again."

    return True, None


# Function to handle registration GET request
def handle_get_request(request):
    action = request.GET.get('action', '')
    if action == 'register':
        return render(request, 'clg/register.html')
    return HttpResponse("<h1>Invalid action</h1>")


# Function to handle OTP verification
def handle_otp_verification(request):
    is_valid, error = validate_otp(request)
    if not is_valid:
        return render(request, 'clg/otp.html', {'email': request.session.get('email'), 'error': error})

    # Proceed with registration
    name = request.session.pop('username', None)
    roll = request.session.pop('rollnumber', None)
    mobile = request.session.pop('mobilenumber', None)
    email = request.session.pop('email', None)
    password = request.session.pop('password', None)

    try:
        student_instance = Student.objects.get(roll_number=roll)


        try:
            Re.objects.create(
                user_name=name,
                password=password,
                roll_number=student_instance,
                mobile_number=mobile,
                email=email
            )
            return render(request, 'clg/success.html', context={'name': name})
        except Exception:
            return HttpResponse("this user already exist")

    except Student.DoesNotExist:
        return HttpResponse("<h1>Student not found with the given roll number.</h1>")



# Function to handle initial registration


def handle_registration(request):
    if request.method == "POST":
        try:
            name = request.POST.get('username')
            roll = request.POST.get('rollnumber').upper()
            mobile = request.POST.get('mobilenumber')
            email = request.POST.get('email')
            password = make_password(request.POST.get('password'))

            # Check if username already exists
            if Re.objects.filter(user_name=name).exists():
                return HttpResponse("<h1>Username Already Exists</h1>")

            # Check if roll number exists in Student table
            try:
                student_data = Student.objects.get(roll_number=roll)
            except Student.DoesNotExist:
                return HttpResponse("<h1>Roll Number Does Not Exist</h1>")

            # Check if email or roll number is already registered
            if Re.objects.filter(email=email).exists():
                return HttpResponse("<h1>Email Already Exists</h1>")

            if Re.objects.filter(roll_number=roll).exists():
                return HttpResponse("<h1>This Roll Number is Already Registered</h1>")

            # Generate OTP and store in session
            otp = str(random.randint(100000, 999999))
            request.session.update({
                'otp': otp,
                'otp_timestamp': now().timestamp(),
                'username': name,
                'rollnumber': student_data.roll_number,
                'mobilenumber': mobile,
                'email': email,
                'password': password,
            })

            # Send OTP email
            send_otp_email(email, otp)

            return render(request, 'clg/otp.html', {'email': email})

        except Exception as e:
            return HttpResponse(f"<h1>Something went wrong: {str(e)}</h1>")

    return HttpResponse("<h1>Invalid Request</h1>")
