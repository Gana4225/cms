from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import *


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

