from django.views.decorators.csrf import csrf_exempt
from .utils import *
from django.http import JsonResponse





def home(request):
    if not check_user_logged_in(request):
        return render(request, 'clg/login.html')
    return redirect('dashboard')


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

    if not check_user_logged_in(request):

        return redirect('home')
    else:
        return redirect('dashboard')

# view for logout
def clogout(request):
    try:

        del request.session['user_id']
        del request.session['last_activity']

    except KeyError:

        pass

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

    try:
        a = request.session.get('user_id')
        b = Re.objects.get(user_name=a)
        c = Student.objects.get(roll_number=b.roll_number)
        if not c.image:
            c.image = None  # You can set a default image URL if needed

        return render(request, 'clg/stdprofile.html', {'student': c, 'a': a})
    except Exception as e:
        print(e)
        return HttpResponse("image error")

def update_profile(request):
    if not check_user_logged_in(request):

        return redirect('home')

    return updatepf(request)
def dd(request):
    return render(request, 'clg/login.html')
