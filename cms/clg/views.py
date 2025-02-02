from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .utils import *
from django.http import JsonResponse




def home(request):

    return render(request, 'clg/login.html')



def heartbeat(request):

    if request.method == "POST" and request.session.get('user_id'):

        request.session.modified = True  # Extend session expiry
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def log(request):

    if request.method == "POST":
        user = request.POST['username']
        password = request.POST['password']

        try:

            data = Re.objects.get(user_name=user)
            if check_password(password, data.password):

                request.session['user_id'] = data.user_name
                request.session['last_activity'] = datetime.now().timestamp()
                return redirect('dashboard')

            else:

                return HttpResponse('invalid password')

        except Exception:

            a = 1
            return render(request, "clg/error.html",
                          context={'user': user, 'a': a})

    else:


        try:

            del request.session['user_id']
            del request.session['last_activity']

        except KeyError:

            pass

        return redirect('home')

    return redirect('home')

# view for user registration

def reg(request):

    if request.method == 'GET':

        return handle_get_request(request)

    if request.method == 'POST':

        if 'otp' in request.POST:

            return handle_otp_verification(request)

        else:

            return handle_registration(request)

    return HttpResponse("<h1>Invalid request method</h1>")





def dashboard(request):

    if not check_user_logged_in(request):

        return redirect('home')

    return render(request, 'clg/dashboard.html')



def about(request):

    if not check_user_logged_in(request):

        return redirect('home')

    return render(request, 'clg/about.html')



def pay(request):

    if not check_user_logged_in(request):

        return redirect('home')

    return redirect('second/')



def otp(request):

    return render(request, 'clg/otp.html')

def stdprofile(request):
    if not check_user_logged_in(request):

        return redirect('home')




    a = request.session.get('user_id')
    b=Re.objects.get(user_name=a)
    c=Student.objects.get(roll_number=b.roll_number)

    return render(request, 'clg/stdprofile.html', {'student':c,'a':a})


from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Re  # Make sure to import the appropriate model
from django.core.files.storage import FileSystemStorage


def update_profile(request):
    if not check_user_logged_in(request):
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        old_password = request.POST.get('old_password')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password == confirm_password:
            encrypted_password = make_password(password)
            try:
                # Get the current user's data using the session user_id
                user = Re.objects.get(user_name=request.session.get('user_id'))

                # Check if the old password matches the stored password
                if check_password(old_password, user.password):
                    user.user_name = username
                    user.password = encrypted_password

                    # Handle profile image upload
                    if 'profile_image' in request.FILES:
                        profile_image = request.FILES['profile_image']

                        # If you want to save the image in a specific location, you can use FileSystemStorage:
                        fs = FileSystemStorage()
                        filename = fs.save(profile_image.name, profile_image)
                        user.image = fs.url(filename)

                    user.save()  # Save the updated data

            except Exception as e:
                print("Error updating profile:", e)
                # You can add a message to inform the user
                return render(request, 'error.html', {'message': 'An error occurred while updating the profile.'})

    return redirect('profile')  # Redirect to the profile page or wherever you want after updating
