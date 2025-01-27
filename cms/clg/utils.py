from datetime import datetime
def check_user_logged_in(request):
    if 'user_id' not in request.session:
        return False

    # Update last activity timestamp
    request.session['last_activity'] = datetime.now().timestamp()
    return True
