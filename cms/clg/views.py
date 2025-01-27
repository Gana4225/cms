from datetime import datetime
from django.shortcuts import render, redirect
from .models import Re
from django.views.decorators.csrf import csrf_exempt
from .utils import check_user_logged_in
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
            if data.password == password:
                request.session['user_id'] = data.id
                request.session['last_activity'] = datetime.now().timestamp()
                return redirect('dashboard')
        except Re.DoesNotExist:
            a = 1
            return render(request, "error.html", context={'user': user, 'pas': password, 'a': a})

    else:
        try:
            del request.session['user_id']
            del request.session['last_activity']
        except KeyError:
            pass
        return redirect('home')
    return redirect('home')

def reg(request):
    if request.method == 'GET':
        action = request.GET.get('action', '')
        if action == 'register':
            return render(request, 'clg/register.html')

    if request.method == 'POST':
        try:
            name = request.POST.get('username')
            roll = request.POST.get('rollnumber')
            mobile = request.POST.get('mobilenumber')
            password = request.POST.get('password')

            Re.objects.create(user_name=name, password=password, roll_number=roll, mobile_number=mobile)
            return render(request, 'clg/success.html', context={'name': name})
        except Exception as e:
            pass

    return render(request, 'clg/success.html')

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
