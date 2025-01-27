import datetime
from django.shortcuts import redirect
from datetime import datetime



class SessionTimeoutMiddleware:
    """
    Middleware to enforce session timeout after 15 minutes of inactivity.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is logged in (based on session key)
        if request.session.get('user_id'):
            last_activity = request.session.get('last_activity')
            now = datetime.now().timestamp()

            # If session has expired (10 seconds for testing, should be 900 for 15 minutes)
            if last_activity and (now - last_activity > 1100):  # 10 seconds for testing
                # Clear session to log out the user
                del request.session['user_id']
                del request.session['last_activity']

                return redirect('home')  # Redirect to the login page

            # Update last activity timestamp if session is still active
            request.session['last_activity'] = now

        response = self.get_response(request)
        return response
